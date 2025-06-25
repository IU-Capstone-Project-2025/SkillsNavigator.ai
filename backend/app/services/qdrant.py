from typing import List
import logging
from qdrant_client import QdrantClient, models
from qdrant_client.conversions import common_types as types

from app.services import run_blocking, encoder

import httpx
import asyncio
import traceback

logger = logging.getLogger(__name__)


class QdrantService:
    def __init__(self):
        self.client = None

    def initialize(self, host: str, port: int):
        logger.info(f"Init Qdrant client on {host}:{port}")
        self.client = QdrantClient(host=host, port=port)
        if not self.client.collection_exists(collection_name="courses"):
            logger.info("Collection 'courses' is not found, try again")
            self.client.create_collection(
                collection_name="courses",
                vectors_config=models.VectorParams(
                    size=encoder.model.get_sentence_embedding_dimension(),
                    distance=models.Distance.COSINE
                ),
            )
        else:
            logger.info("Collection 'courses' already exists")

    async def search(self, query: List[float], collection_name: str, limit: int = 10) -> List[dict]:
        logger.info(f"Search in collection '{collection_name}' with limit {limit}")
        try:
            result = await run_blocking(
                self.client.query_points,
                collection_name=collection_name,
                query=query,
                limit=limit
            )
            logger.info(f"Found {len(result.points)} similar")
            return result.points
        except Exception as e:
            logger.exception("Error Searching in Qdrant")
            raise

    async def loadCourses(self):
        logger.info("Load courses from Stepik")
        async with httpx.AsyncClient(timeout=None) as client:
            courses = {}
            courses_ids_set = set()
            points = []
            page = 1

            try:
                while True:
                    logger.info(f"Getting page courses list: {page}")
                    res = await client.get(f"https://stepik.org/api/course-lists?page={page}")
                    course_lists = res.json()
                    for section in course_lists["course-lists"]:
                        logger.info(f"Getting courses from: {section['title']}")
                        courses_ids_set.update(section["courses"])

                    if not course_lists['meta']['has_next']:
                        break
                    page += 1

                logger.info(f"Found {len(courses_ids_set)} unique courses")

                courses_ids_list = list(courses_ids_set)
                for i in range(0, len(courses_ids_list), 100):
                    subset = courses_ids_list[i:i + 100]
                    logger.info(f"Processing courses: {i} - {i + len(subset)}")
                    params = {'ids[]': subset}
                    res = await client.get("https://stepik.org/api/courses", params=params)
                    course_data = res.json()["courses"]

                    review_ids = []
                    author_ids = []

                    for course_info in course_data:
                        if course_info["authors"]:
                            author_ids.append(course_info["authors"][0])
                        review_ids.append(course_info["review_summary"])
                        courses[course_info["id"]] = {
                            "id": course_info["id"],
                            "cover_url": course_info["cover"],
                            "title": course_info["title"],
                            "duration": int(course_info["time_to_complete"] / 3600) if course_info[
                                "time_to_complete"] else 0,
                            "difficulty": course_info["difficulty"],
                            "price": 0 if course_info["price"] is None else course_info["price"],
                            "currency_code": course_info["currency_code"],
                            "pupils_num": course_info["learners_count"],
                            "authors": course_info["authors"][0] if course_info["authors"] else "",
                            "rating": 5,
                            "url": f"https://stepik.org/course/{course_info['id']}/promo",
                            "description": course_info["description"],
                            "summary": course_info["summary"],
                            "target_audience": course_info["target_audience"],
                            "acquired_skills": ''.join(course_info["acquired_skills"]),
                            "acquired_assets": ''.join(course_info["acquired_assets"]),
                            "title_en": course_info["title_en"],
                            "learning_format": course_info["learning_format"],
                        }

                    logger.info("Getting course ratings")
                    reviews = (await client.get("https://stepik.org/api/course-review-summaries",
                                                params={'ids[]': review_ids})).json()
                    for review in reviews["course-review-summaries"]:
                        if review["course"] in courses:
                            courses[review["course"]]["rating"] = int(review["average"])

                    logger.info("Getting authors info")
                    authors = (await client.get("https://stepik.org/api/users", params={'ids[]': author_ids})).json()
                    for author in authors["users"]:
                        for i in courses:
                            if courses[i]["authors"] == author["id"]:
                                courses[i]["authors"] = author["full_name"]
                    for i in courses:
                        if str(courses[i]["authors"]).isdigit():
                            courses[i]["authors"] = ""

                    logger.info("Starting course vectorization")
                    for course in courses.values():
                        vector = await encoder.vectorize(
                            f"Название: {course['title']} ({course['title_en']})\n"
                            f"Сложность: {course['difficulty']}\n"
                            f"Резюме: {course['summary']}"
                        )
                        points.append(models.PointStruct(id=course["id"], vector=vector, payload=course))

                    logger.info(f"Loaded {len(points)} dots in Qdrant")
                    self.client.upload_points(collection_name="courses", points=points)

                    courses.clear()
                    points.clear()

                logger.info("Successful course download to Qdrant")

            except Exception as e:
                logger.exception("Error Loading to Qdrant")
                raise


qdrant = QdrantService()

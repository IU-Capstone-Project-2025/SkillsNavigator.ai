from typing import List

from qdrant_client import QdrantClient, models
from qdrant_client.conversions import common_types as types

from app.services import run_blocking, encoder

import httpx
import asyncio
import traceback


class QdrantService:
    def __init__(self):
        self.client = None

    def initialize(self, host: str, port: int):
        self.client = QdrantClient(host=host, port=port)
        if not self.client.collection_exists(collection_name="courses"):
            self.client.create_collection(
                collection_name="courses",
                vectors_config=models.VectorParams(size=encoder.model.get_sentence_embedding_dimension(),
                                                   distance=models.Distance.COSINE),
            )

    async def search(self, query: List[float], collection_name: str, limit: int = 10) -> List[dict]:
        return (await run_blocking(self.client.query_points,
                                   collection_name=collection_name,
                                   query=query,
                                   limit=limit
                                   )).points

    async def loadCourses(self):
        print("Loading Courses from stepik", flush=True)
        async with httpx.AsyncClient(timeout=None) as client:
            courses = {}
            courses_ids_set = set()
            points = []
            page = 1
            while True:
                print(f"page={page}", flush=True)

                courses_list_req = await client.get(f"https://stepik.org/api/course-lists?page={page}")

                courses_list = courses_list_req.json()

                for i in range(len(courses_list["course-lists"])):
                    course_section = courses_list["course-lists"][i]
                    print("Getting courses in " + course_section["title"], flush=True)
                    courses_ids_set.update(course_section["courses"])

                print(f"Current size: {len(courses_ids_set)}", flush=True)

                if not courses_list['meta']['has_next']:
                    break
                page += 1

            # We have list of all stepik courses. Now we need to get info about them.

            courses_ids_list = list(courses_ids_set)

            for i in range(0, len(courses_ids_list), 100):
                print(f"Page: {i}", flush=True)
                subset = courses_ids_list[i:i + 100]
                params = {'ids[]': subset}
                courses_info_req = await client.get("https://stepik.org/api/courses", params=params)
                courses_info = courses_info_req.json()["courses"]
                    # ratings_info_req = await client.get(f"https://stepik.org/api/course-review-summaries", params=params)
                    # ratings_info = ratings_info_req.json()["course-review-summaries"]
                review_ids = []
                author_ids = []
                try:
                    for k in range(len(courses_info)):
                        course_info = courses_info[k]
                        if len(course_info["authors"]) > 0:
                            author_ids.append(course_info["authors"][0])
                        review_ids.append(course_info["review_summary"])
                        # rating_info = ratings_info[k]
                        courses[course_info["id"]] = {
                        # Payload
                        "id": course_info["id"],
                        "cover_url": course_info["cover"],
                        "title": course_info["title"],
                        "duration": course_info["time_to_complete"],
                        "difficulty": course_info["difficulty"],
                        "price": 0 if course_info["price"] is None else course_info["price"],
                        "currency_code": course_info["currency_code"],
                        "pupils_num": course_info["learners_count"],
                        "authors":  course_info["authors"][0] if len(course_info["authors"]) > 0 else "", # парсить авторов
                        "rating": 5,
                        "url": f"https://stepik.org/course/{course_info['id']}/promo",
                        "description": course_info["description"],
                        "summary": course_info["summary"],
                        "target_audience": course_info["target_audience"],
                        "acquired_skills": ''.join(course_info["acquired_skills"]),
                        "acquired_assets": ''.join(course_info["acquired_assets"]),
                        "title_en": course_info["title_en"],
                        "learning_format": course_info["learning_format"],
                        # "section_desc": course_section["description"],
                        }

                    print(f"Getting reviews", flush=True)
                    params = {'ids[]': review_ids}
                    reviews = (await client.get("https://stepik.org/api/course-review-summaries", params=params)).json()
                    for review_c in range(len(reviews["course-review-summaries"])):
                        review = reviews["course-review-summaries"][review_c]
                        courses[review["course"]]["rating"] = review["average"]

                    print(f"Getting authors", flush=True)
                    params = {'ids[]': author_ids}
                    authors = (await client.get("https://stepik.org/api/users", params=params)).json()
                    for author_c in range(len(authors["users"])):
                        for i in courses:
                            if courses[i]["authors"] == authors["users"][author_c]["id"]:
                                courses[i]["authors"] = authors["users"][author_c]["full_name"]
                                break      

                except Exception as e:
                    print(e, flush=True)
                    print(traceback.format_exc(), flush=True)    

                print(f"Start vectorization", flush=True)
                for course in courses.values():
                    vector = await encoder.vectorize(f"Название: {course['title']} ({course['title_en']})\n"
                        f"Сложность: {course['difficulty']}\n"
                        f"Резюме: {course['summary']}")
                        # Create a point for the course
                    points.append(models.PointStruct(
                        id=course["id"],
                        vector=vector,
                        payload=course
                    ))
                print("Uploading..", flush=True)
                self.client.upload_points(
                    collection_name="courses",
                    points=points,
                    )
                courses.clear()
                points.clear()

        print('Courses loaded', flush=True)


qdrant = QdrantService()

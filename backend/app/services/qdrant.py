from typing import List

from qdrant_client import QdrantClient, models
from qdrant_client.conversions import common_types as types

from app.services import run_blocking, encoder

import httpx


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
            courses = []
            points = []
            page = 1
            while True:
                print(f"page={page}", flush=True)

                courses_list_req = await client.get(f"https://stepik.org/api/course-lists?page={page}")

                courses_list = courses_list_req.json()

                for i in range(len(courses_list["course-lists"])):
                    course_section = courses_list["course-lists"][i]
                    for z in range(len(course_section["courses"]) // 100 + 1):
                        params = {'ids[]': course_section["courses"][100 * z:100 * (z + 1)]}
                        print("Getting courses in " + course_section["title"], flush=True)
                        courses_info_req = await client.get("https://stepik.org/api/courses", params=params)
                        courses_info = courses_info_req.json()["courses"]
                        # ratings_info_req = await client.get(f"https://stepik.org/api/course-review-summaries", params=params)
                        # ratings_info = ratings_info_req.json()["course-review-summaries"]
                        try:
                            for k in range(len(courses_info)):
                                course_info = courses_info[k]
                                # rating_info = ratings_info[k]
                                courses.append({
                                    # Payload
                                    "id": course_info["id"],
                                    "cover_url": course_info["cover"],
                                    "title": course_info["title"],
                                    "duration": course_info["time_to_complete"],
                                    "difficulty": course_info["difficulty"],
                                    "price": 0 if course_info["price"] is None else course_info["price"],
                                    "currency_code": "RUB" if course_info["currency_code"] is None else course_info["currency_code"],
                                    "pupils_num": course_info["learners_count"],
                                    "authors": [], # парсить авторов
                                    "rating": 5, # парсить рейтинг
                                    "url": f"https://stepik.org/course/{course_info['id']}/promo",
                                    "description": course_info["description"],
                                    "summary": course_info["summary"],
                                    "target_audience": course_info["target_audience"],
                                    "acquired_skills": ''.join(course_info["acquired_skills"]),
                                    "acquired_assets": ''.join(course_info["acquired_assets"]),
                                    "title_en": course_info["title_en"],
                                    "learning_format": course_info["learning_format"],
                                    # "section_desc": course_section["description"],
                                })
                        except Exception as e:
                            print(e, flush=True)
                    for idx, course in enumerate(courses):
                        vector = await encoder.vectorize(f"Название: {course['title']} ({course['title_en']})\n"
                                                         f"Сложность: {course['difficulty']}\n"
                                                         f"Резюме: {course['summary']}")

                        # Create a point for the course
                        points.append(models.PointStruct(
                            id=course["id"],
                            vector=vector,
                            payload=course
                        ))

                    self.client.upload_points(
                        collection_name="courses",
                        points=points,
                    )
                    courses.clear()
                    points.clear()
                if not courses_list['meta']['has_next']:
                    break
                page += 1

            print("Creating collection", flush=True)

        print('Courses loaded', flush=True)


qdrant = QdrantService()

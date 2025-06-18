from typing import List

from qdrant_client import QdrantClient, models

from app.services import run_blocking, encoder

import requests

class QdrantService:
    def __init__(self):
        self.client = None

    def initialize(self, host: str, port: int):
        self.client = QdrantClient(host=host, port=port)
        if not self.client.collection_exists(collection_name="courses"):
            self.client.create_collection(
                collection_name="courses",
                vectors_config=models.VectorParams(size=encoder.model.get_sentence_embedding_dimension(), distance=models.Distance.COSINE),
            )

    async def search(self, query: List[float], collection_name: str, limit: int = 10) -> List[dict]:
        return (await run_blocking(self.client.query_points,
            collection_name=collection_name,
            query=query,
            limit=limit
        )).points
        
    async def loadCourses(self, collection_name):
        print("Loading Courses from stepik")
        courses_list_req = requests.get("https://stepik.org/api/course-lists")
        courses_list = courses_list_req.json()

        courses = []
        points = []  # Инициализация списка для точек
        # TODO: Загружать курсы с других страниц
        for i in range(len(courses_list["course-lists"])):
            course_section = courses_list["course-lists"][i]
            params = {'ids[]': course_section["courses"]}
            print("Getting courses in " + course_section["title"]) 
            courses_info_req = requests.get("https://stepik.org/api/courses/", params=params)
            courses_info = courses_info_req.json()["courses"]
    
            for k in range(len(courses_info)):
                course_info = courses_info[k]
                courses.append({
                # Payload
                "id": course_info["id"],
                "title": course_info["title"],
                "difficulty": course_info["difficulty"],
                # Embeddings
                "description": course_info["description"],
                "summary": course_info["summary"],
                "target_audience": course_info["target_audience"],
                "acquired_skills": ''.join(course_info["acquired_skills"]),
                "acquired_assets": ''.join(course_info["acquired_assets"]),
                "title_en": course_info["title_en"],
                "learning_format": course_info["learning_format"],
                "section_desc": course_section["description"]
            })
        
        for idx, course in enumerate(courses):
            # summary_vector = encoder.vectorize(course["summary"]).tolist()
            # target_audience_vector = encoder.vectorize(course["target_audience"]).tolist()
            # acquired_assets_vector = encoder.vectorize(course["acquired_assets"]).tolist()
            # learning_format_vector = encoder.vectorize(course["learning_format"]).tolist()
            # section_desc_vector = encoder.vectorize(course["description"]).tolist()
    
            combined_vector = (
                encoder.vectorize(course["description"])
            )
    
            # Create a point for the course
            points.append(encoder.model.PointStruct(
                id=course["id"],
                vector=combined_vector,
                payload=course
            ))
            
            self.client.upload_points(
                collection_name=collection_name,
                points=points,
            )
    print('Courses loaded')


qdrant = QdrantService()
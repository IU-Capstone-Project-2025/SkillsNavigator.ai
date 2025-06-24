from fastapi import APIRouter, HTTPException, Body
from typing import List

from app.models import *
from app.services import qdrant, encoder

import traceback
import httpx

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.post(
    "/search",
    response_model=List[CourseSummary],
    summary="Поиск курсов по заданным критериям"
)
async def search_courses(payload: CourseSearchRequest = Body(...)):
    """
    Поиск курсов:
    1. **area** — область знаний, которую хочет освоить пользователь
    2. **current_level** — текущий уровень (начальный/средний/продвинутый)
    3. **desired_skills** — конкретные навыки для обучения
    """
    results = [course.payload for course in await qdrant.search(
        await encoder.vectorize(payload.area + " " + payload.current_level + " " + payload.desired_skills),
        "courses"
    )]

    if not results:
        raise HTTPException(status_code=404, detail="Курсы не найдены")
    return results


@router.get(
    "/popular",
    response_model=List[CourseSummary],
    summary="Get popular courses"
)
async def get_popular_courses():
    """
    Возвращает список самых популярных курсов.
    """

    # TODO: Fetch popular courses from postgresql.
    async with httpx.AsyncClient(timeout=None) as client:
        courses_ids_set = list()
        req = await client.get("https://stepik.org/api/course-recommendations")
        courses_ids_set = req.json()["course-recommendations"][0]["courses"]
        courses = {}
        params = {'ids[]': courses_ids_set}
        courses_info_req = await client.get("https://stepik.org/api/courses", params=params)
        courses_info = courses_info_req.json()["courses"]
        review_ids = []
        author_ids = []
        try:
            for k in range(len(courses_info)):
                course_info = courses_info[k]
                if len(course_info["authors"]) > 0:
                    author_ids.append(course_info["authors"][0])
                review_ids.append(course_info["review_summary"])
                courses[course_info["id"]] = {
                "id": course_info["id"],
                "cover_url": course_info["cover"],
                "title": course_info["title"],
                "duration": int(course_info["time_to_complete"]/3600) if course_info["time_to_complete"] else 0,
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
                }

            params = {'ids[]': review_ids}
            reviews = (await client.get("https://stepik.org/api/course-review-summaries", params=params)).json()
            for review_c in range(len(reviews["course-review-summaries"])):
                review = reviews["course-review-summaries"][review_c]
                courses[review["course"]]["rating"] = int(review["average"])

            params = {'ids[]': author_ids}
            authors = (await client.get("https://stepik.org/api/users", params=params)).json()
            for author_c in range(len(authors["users"])):
                for i in courses:
                    if courses[i]["authors"] == authors["users"][author_c]["id"]:
                        courses[i]["authors"] = authors["users"][author_c]["full_name"]      
            for i in courses:
                    if courses[i]["authors"].isdigit():
                        courses[i]["authors"] = ""

        except Exception as e:
            print(e, flush=True)
            print(traceback.format_exc(), flush=True)    
            raise HTTPException(status_code=500)
        
        results = courses.values()

    if not results:
        raise HTTPException(status_code=404, detail="Популярные курсы не найдены")
    return results

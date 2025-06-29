from fastapi import APIRouter, HTTPException, Body
from typing import List

from app.models import *
from app.services import qdrant, encoder

import traceback
import httpx
import logging

logger = logging.getLogger(__name__)
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
    logger.info(
        f"Search courses: area='{payload.area}', level='{payload.current_level}', slills='{payload.desired_skills}'"
    )

    try:
        query_text = f"{payload.area} {payload.current_level} {payload.desired_skills}"
        vector = await encoder.vectorize(query_text)
        results = [course.payload for course in await qdrant.search(vector, "courses")]

        if not results:
            logger.warning("No search results")
            raise HTTPException(status_code=404, detail="Курсы не найдены")

        logger.info(f"Found {len(results)} courses")
        return results

    except Exception as e:
        logger.exception(f"Error course searching: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/popular",
    response_model=List[CourseSummary],
    summary="Get popular courses"
)
async def get_popular_courses():
    """
    Возвращает список самых популярных курсов.
    """

    logger.info("Requesting popular courses")

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            logger.info("Send request to Stepik: course-recommendations")
            req = await client.get("https://stepik.org/api/course-recommendations")
            courses_ids_set = req.json()["course-recommendations"][0]["courses"]
            logger.info(f"Got {len(courses_ids_set)} courses")

            params = {'ids[]': courses_ids_set}
            logger.info("Request detailed course info")
            courses_info_req = await client.get("https://stepik.org/api/courses", params=params)
            courses_info = courses_info_req.json()["courses"]

            review_ids = []
            author_ids = []
            courses = {}

            for course_info in courses_info:
                if course_info["authors"]:
                    author_ids.append(course_info["authors"][0])
                review_ids.append(course_info["review_summary"])
                courses[course_info["id"]] = {
                    "id": course_info["id"],
                    "cover_url": course_info["cover"],
                    "title": course_info["title"],
                    "duration": int(course_info["time_to_complete"] / 3600) if course_info["time_to_complete"] else 0,
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

            logger.info("Get rating via review_summary")
            reviews = (await client.get("https://stepik.org/api/course-review-summaries", params={'ids[]': review_ids})).json()
            for review in reviews["course-review-summaries"]:
                if review["course"] in courses:
                    courses[review["course"]]["rating"] = int(review["average"])

            logger.info("Get authors info")
            authors = (await client.get("https://stepik.org/api/users", params={'ids[]': author_ids})).json()
            for author in authors["users"]:
                for i in courses:
                    if courses[i]["authors"] == author["id"]:
                        courses[i]["authors"] = author["full_name"]

            for i in courses:
                if str(courses[i]["authors"]).isdigit():
                    courses[i]["authors"] = ""

        results = list(courses.values())
        if not results:
            logger.warning("Popular courses not found")
            raise HTTPException(status_code=404, detail="Popular courses not found")

        logger.info(f"Return {len(results)} popular courses")
        return results

    except Exception as e:
        logger.exception("Error getting popular courses")
        raise HTTPException(status_code=500, detail="Internal Server Error")

from fastapi import APIRouter, HTTPException, Body
from typing import List

from app.models import *
from app.services import qdrant, encoder

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
    # заменить на реальную логику выборки из БД,
    # например: results = await fetch_popular_courses_from_db()
    results = [
        {
            "id": 10,
            "cover_url": "https://avatars.mds.yandex.net/i?id=a5be1a85e5edf3a1d698f82857ed4926_l-5332940-images-thumbs&n=13",
            "title": "Mastering Python",
            "duration": 40,
            "difficulty": "medium",
            "price": 2500,
            "pupils_num": 1200,
            "authors": "Alice Ivanova",
            "rating": 5,
            "url": "https://example.com/course/10"
        },
        {
            "id": 22,
            "cover_url": "https://avatars.mds.yandex.net/i?id=a5be1a85e5edf3a1d698f82857ed4926_l-5332940-images-thumbs&n=13",
            "title": "Advanced FastAPI",
            "duration": 16,
            "difficulty": "hard",
            "price": 3500,
            "pupils_num": 800,
            "authors": "Bob Petrov, Carol Smirnov",
            "rating": 5,
            "url": "https://example.com/course/22"
        }
    ]

    if not results:
        raise HTTPException(status_code=404, detail="Популярные курсы не найдены")
    return results

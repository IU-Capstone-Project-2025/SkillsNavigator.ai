from fastapi import APIRouter, HTTPException, Body
from typing import List

from app.models import *


router = APIRouter(prefix="/courses", tags=["courses"])


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
    # Здесь реальная логика:
    # results = await fetch_courses_from_db(
    #     area=payload.area,
    #     current_level=payload.current_level,
    #     desired_skills=payload.desired_skills
    # )

    # Для примера возвращаем статичный список
    results = [
        {
            "id": 1,
            "cover_url": "https://avatars.mds.yandex.net/i?id=a5be1a85e5edf3a1d698f82857ed4926_l-5332940-images-thumbs&n=13",
            "title": "FastAPI for Beginners",
            "duration": 8,
            "difficulty": "easy",  # лёгкий/средний/сложный
            "price": 1000,
            "pupils_num": 150,
            "authors": ["Arthur", "Didi"],
            "rating": 5,
            "url": "https://letmegooglethat.com/what_is_fastAPI"
        }
    ]

    if not results:
        raise HTTPException(status_code=404, detail="Курсы не найдены")
    return results

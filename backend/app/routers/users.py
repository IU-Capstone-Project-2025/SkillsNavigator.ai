from fastapi import APIRouter, HTTPException, Body
from typing import List

from app.models import *

router = APIRouter()


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.post(
    "/courses/search",
    response_model=CourseSummary,
    tags=["courses"],
    summary="Поиск курсов по заданным критериям"
)
async def search_courses(payload: CourseSearchRequest = Body(...)):
    """
    Поиск курсов:
    1. **area** — область знаний, которую хочет освоить пользователь
    2. **current_level** — текущий уровень (начальный/средний/продвинутый)
    3. **desired_skills** — конкретные навыки для обучения
    """
    """
    results = await fetch_courses_from_db(
        area=payload.area,
        current_level=payload.current_level,
        desired_skills=payload.desired_skills
    )
    """
    results = {
        "id": 1,
        "title": "NoNoNo Mr. Fish",
        "duration": 8,  # в часа
        "difficulty": "haaard",  # лёгкий/средний/сложный
        "price": 1000,  # в рублях или другой валюте
        "authors": ["Arthur", "Didi"],  # можно отдавать пустой список, детали подтягивать позже
        "rating": 8,  # 0–5
        "url": "https://letmegooglethat.com/what_is_fastAPI"
    }
    if results is None:
        raise HTTPException(status_code=404, detail="Курсы не найдены")
    return results

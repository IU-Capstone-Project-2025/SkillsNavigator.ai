from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel, Field
from datetime import datetime
from app.services import database
from app.models.roadmap import Course 

# Модель запроса от фронта
class CourseSearchRequest(BaseModel):
    area: str
    current_level: str
    desired_skills: str
    chat_id: Optional[int] = Field(None)

# Модель одного курса в ответе
class CourseSummary(BaseModel):
    id: int
    cover_url: Optional[str]        # ссылка на обложку курса
    title: str
    duration: Optional[int]         # в часах
    difficulty: Optional[str]       # лёгкий/средний/сложный
    price: int            # цена курса
    currency_code: Optional[str]    # в чём валюта в рублях долларах и т.д.
    pupils_num: int       # количество записавшихся учеников
    authors: str    # можно отдавать пустой список, детали подтягивать позже
    rating: int           # 0–5
    url: str
    description: str # описание курса
    summary: str
    target_audience: str
    acquired_skills: str
    acquired_assets: str
    title_en: str
    learning_format: str
    # section_desc: str # описание секции курса


def course_summary_to_model(course_summary: CourseSummary) -> Course:
    return Course(
        id=course_summary.id,
        cover_url=course_summary.cover_url,
        title=course_summary.title,
        duration=course_summary.duration,
        difficulty=course_summary.difficulty,
        price=course_summary.price,
        currency_code=course_summary.currency_code,
        pupils_num=course_summary.pupils_num,
        authors=course_summary.authors,
        rating=course_summary.rating,
        url=course_summary.url,
        description=course_summary.description,
        summary=course_summary.summary,
        target_audience=course_summary.target_audience,
        acquired_skills=course_summary.acquired_skills,
        acquired_assets=course_summary.acquired_assets,
        title_en=course_summary.title_en,
        learning_format=course_summary.learning_format,
    )
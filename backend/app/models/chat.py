from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime

# Модель запроса от фронта
class CourseSearchRequest(BaseModel):
    area: str
    current_level: str
    desired_skills: str

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
    authors: List[str]    # можно отдавать пустой список, детали подтягивать позже
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
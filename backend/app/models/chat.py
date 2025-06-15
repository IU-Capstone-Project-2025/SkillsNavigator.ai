from typing import List

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
    title: str
    duration: int        # в часах
    difficulty: str      # лёгкий/средний/сложный
    price: int           # в рублях или другой валюте
    authors: List[str]   # можно отдавать пустой список, детали подтягивать позже
    rating: int          # 0–5
    url: str
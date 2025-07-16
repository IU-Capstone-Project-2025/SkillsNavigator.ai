from typing import List, Optional
from pydantic import BaseModel


class RoadmapRequest(BaseModel):
    area: str
    current_level: str
    desired_skills: str
    include_courses: bool = True


class SkillNode(BaseModel):
    skill: str
    sub_skills: List[str]
    difficulty: str
    estimated_time: str
    prerequisites: List[str] = []


class LearningStep(BaseModel):
    step_number: int
    title: str
    description: str
    skills: List[SkillNode]
    estimated_duration: str
    difficulty: str


class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None


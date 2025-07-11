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


class RoadmapResponse(BaseModel):
    title: str
    description: str
    total_estimated_time: str
    difficulty_progression: str
    steps: List[LearningStep]
    courses: Optional[List[dict]] = None  # Will contain course recommendations


class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    roadmap: Optional[RoadmapResponse] = None
    courses: Optional[List[dict]] = None

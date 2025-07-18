from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.roadmap import RoadmapStatus
from app.schemas.course import CourseSummary


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

class MessageSchema(BaseModel):
    id: int
    text: str
    is_user: bool
    dialog_id: int

    class Config:
        orm_mode = True


class RoadmapSchema(BaseModel):
    id: int
    status: RoadmapStatus
    name: str
    courses: List[CourseSummary] = Field(default_factory=list)

    class Config:
        orm_mode = True

class DialogSchema(BaseModel):
    id: int
    name: Optional[str] = None
    owner: int
    roadmap_id: Optional[int] = None
    messages: List[MessageSchema] = Field(default_factory=list)

    class Config:
        orm_mode = True
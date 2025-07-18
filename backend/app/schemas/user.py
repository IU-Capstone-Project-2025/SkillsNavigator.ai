from typing import List, Optional
from pydantic import BaseModel

class UserInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    avatar: Optional[str]

    class Config:
        orm_mode = True
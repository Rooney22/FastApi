from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    username: str
    password_hashed: str
    role: str
    created_by: int
    created_at: datetime
    modified_by: int
    modified_at: datetime

    class Config:
        orm_mode = True

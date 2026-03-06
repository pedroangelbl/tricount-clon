import uuid
from pydantic import BaseModel
from datetime import datetime


class MemberCreate(BaseModel):
    display_name: str
    group_id: uuid.UUID

class MemberUpdate(BaseModel):
    display_name: str


class MemberResponse(BaseModel):
    id: uuid.UUID
    display_name: str
    role: str
    joined_at: datetime
    group_id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        from_attributes = True
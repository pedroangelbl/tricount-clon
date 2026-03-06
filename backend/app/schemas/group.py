import uuid
from pydantic import BaseModel
from datetime import datetime

from app.schemas.member import MemberResponse

class GroupCreate(BaseModel):
    name: str
    description: str | None = None
    created_by: uuid.UUID

class GroupUpdate(BaseModel):
    name: str
    description: str | None = None


class GroupResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    created_by: uuid.UUID
    created_at: datetime
    
    members: list[MemberResponse]

    class Config:
        from_attributes = True
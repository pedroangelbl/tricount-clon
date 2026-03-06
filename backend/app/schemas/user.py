import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime


# Schema para creación de usuario
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserUpdate(BaseModel):
    username: str
    email: EmailStr | None = None  # opcional
    password: str | None = None


# Schema para mostrar al frontend (sin password)
class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # Permite usar objetos SQLAlchemy directamente
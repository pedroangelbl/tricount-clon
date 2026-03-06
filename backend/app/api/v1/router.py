# Este el punto de conexion de todos los routers

from fastapi import APIRouter
from app.api.v1.endpoints import users
from app.api.v1.endpoints import groups
from app.api.v1.endpoints import members
from app.api.v1.endpoints import expenses
from app.api.v1.endpoints import auth

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(groups.router)
api_router.include_router(members.router)
api_router.include_router(expenses.router)
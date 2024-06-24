from fastapi import APIRouter

from src.user.router import auth_router
from src.user.router import user_router


api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(user_router)

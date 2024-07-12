from fastapi import APIRouter

from src.routers.auth import router as auth_router
from src.routers.user import router as user_router
from src.routers.api_provider import router as api_providers_router
from src.routers.api_key import router as api_key_router


api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(api_providers_router)
api_router.include_router(api_key_router)

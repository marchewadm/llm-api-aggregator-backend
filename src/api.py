from fastapi import APIRouter

from src.auth.router import router as auth_router
from src.user.router import router as user_router
from src.api_provider.router import router as api_providers_router
from src.api_key.router import router as api_key_router
from src.chat_room.router import router as chat_room_router
from src.chat_history.router import router as chat_history_router

from src.openai.router import router as openai_router
from src.gemini.router import router as gemini_router


api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(api_providers_router)
api_router.include_router(api_key_router)
api_router.include_router(chat_room_router)
api_router.include_router(chat_history_router)
api_router.include_router(openai_router)
api_router.include_router(gemini_router)

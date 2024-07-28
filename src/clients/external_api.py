from fastapi import APIRouter

from .routers.openai import router as openai_router


external_api_router = APIRouter(prefix="/external")

external_api_router.include_router(openai_router)

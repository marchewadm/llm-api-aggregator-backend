from fastapi import APIRouter

from .services.service import load_ai_models

from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency

from .schemas.schemas import AiModelResponseCollection
from src.openapi.responses import get_ai_models_responses


router = APIRouter(prefix="/ai-models", tags=["ai-models"])


@router.get(
    "/",
    response_model=AiModelResponseCollection,
    responses={**get_ai_models_responses},
)
async def get_ai_models(auth: auth_dependency, db: db_dependency):
    result = load_ai_models(db, auth["id"])
    return result

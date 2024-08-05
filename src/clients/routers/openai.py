from fastapi import APIRouter

from src.dependencies import AuthDependency
from src.clients.external_dependencies import (
    OpenAiServiceDependency,
    OpenAiApiKeyDependency,
)
from src.clients.schemas.common import AiModelsResponse


router = APIRouter(prefix="/openai", tags=["openai"])


@router.get("/models", response_model=AiModelsResponse)
async def get_openai_models(
    auth: AuthDependency,
    api_key: OpenAiApiKeyDependency,
    openai_service: OpenAiServiceDependency,
):
    """
    Get the available OpenAI models.
    """

    return openai_service.get_ai_models()

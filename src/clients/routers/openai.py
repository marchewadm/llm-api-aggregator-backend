from fastapi import APIRouter

from src.dependencies import AuthDependency
from src.clients.external_dependencies import (
    OpenAiServiceDependency,
    OpenAiApiKeyDependency,
)


router = APIRouter(prefix="/openai", tags=["openai"])


@router.get("/models")
async def get_openai_models(
    auth: AuthDependency,
    api_key: OpenAiApiKeyDependency,
    openai_service: OpenAiServiceDependency,
):
    """
    Get the available OpenAI models.
    """

    return await openai_service.get_models(api_key)

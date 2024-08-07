from fastapi import APIRouter

from src.dependencies import (
    AuthDependency,
    OpenAiServiceDependency,
    OpenAiApiKeyDependency,
)

from src.schemas.common import AiModelsResponse
from src.schemas.openai import (
    OpenAiChatCompletionRequest,
    OpenAiChatCompletionResponse,
)


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


@router.post("/chat", response_model=OpenAiChatCompletionResponse)
async def chat_with_openai(
    auth: AuthDependency,
    api_key: OpenAiApiKeyDependency,
    openai_service: OpenAiServiceDependency,
    payload: OpenAiChatCompletionRequest,
):
    """
    Chat with OpenAI using the specified model.
    """

    return await openai_service.chat(api_key, payload)

from fastapi import APIRouter

from src.shared.schemas.common import AiModelsResponse

from src.auth.dependencies import AuthDependency
from src.chat_room.dependencies import ChatRoomServiceDependency
from .dependencies import OpenAiServiceDependency, OpenAiApiKeyDependency

from .schemas import OpenAiChatCompletionRequest, OpenAiChatCompletionResponse


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
    chat_room_service: ChatRoomServiceDependency,
    payload: OpenAiChatCompletionRequest,
):
    """
    Send message to OpenAI's model and get response from it.
    """

    return await openai_service.chat(
        auth.user_id, api_key, payload, chat_room_service
    )

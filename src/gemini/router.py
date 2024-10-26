from fastapi import APIRouter

from src.shared.schemas import (
    ChatHistoryCompletionRequest,
    ChatHistoryCompletionResponse,
)

from src.auth.dependencies import AuthDependency
from src.chat_room.dependencies import ChatRoomServiceDependency
from src.chat_history.dependencies import ChatHistoryServiceDependency
from .dependencies import GeminiApiKeyDependency, GeminiServiceDependency


router = APIRouter(prefix="/gemini", tags=["gemini"])


@router.post("/chat", response_model=ChatHistoryCompletionResponse)
async def chat_with_gemini(
    auth: AuthDependency,
    api_key: GeminiApiKeyDependency,
    gemini_service: GeminiServiceDependency,
    chat_room_service: ChatRoomServiceDependency,
    chat_history_service: ChatHistoryServiceDependency,
    payload: ChatHistoryCompletionRequest,
):
    """
    Send message to Google Gemini's model and get response from it.
    """

    return await gemini_service.chat(
        auth.user_id, api_key, chat_room_service, chat_history_service, payload
    )

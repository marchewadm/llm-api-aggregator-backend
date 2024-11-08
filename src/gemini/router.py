from fastapi import APIRouter, UploadFile

from src.shared.schemas import (
    ChatHistoryCompletionRequest,
    ChatHistoryCompletionResponse,
    ChatHistoryUploadImageResponse,
)

from src.auth.dependencies import AuthDependency
from src.chat_room.dependencies import ChatRoomServiceDependency
from src.chat_history.dependencies import ChatHistoryServiceDependency
from .dependencies import GeminiApiKeyDependency, GeminiServiceDependency


router = APIRouter(prefix="/gemini", tags=["gemini"])


@router.post("/upload-image", response_model=ChatHistoryUploadImageResponse)
async def upload_image(
    auth: AuthDependency,
    gemini_service: GeminiServiceDependency,
    image: UploadFile,
):
    """
    Upload image to S3 and return the URL to use it in the chat message.
    """

    return await gemini_service.upload_image(image)


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

from fastapi import APIRouter, UploadFile

from src.shared.schemas import (
    ChatHistoryCompletionRequest,
    ChatHistoryCompletionResponse,
    ChatHistoryUploadImageResponse,
)

from src.auth.dependencies import AuthDependency
from src.chat_room.dependencies import ChatRoomServiceDependency
from src.chat_history.dependencies import ChatHistoryServiceDependency
from .dependencies import OpenAiServiceDependency, OpenAiApiKeyDependency


router = APIRouter(prefix="/openai", tags=["openai"])


@router.post("/upload-image", response_model=ChatHistoryUploadImageResponse)
async def upload_image(
    auth: AuthDependency,
    openai_service: OpenAiServiceDependency,
    image: UploadFile,
):
    """
    Upload image to S3 and return the URL to use it in the chat message.
    """

    return await openai_service.upload_image(image)


@router.post("/chat", response_model=ChatHistoryCompletionResponse)
async def chat_with_openai(
    auth: AuthDependency,
    api_key: OpenAiApiKeyDependency,
    openai_service: OpenAiServiceDependency,
    chat_room_service: ChatRoomServiceDependency,
    chat_history_service: ChatHistoryServiceDependency,
    payload: ChatHistoryCompletionRequest,
):
    """
    Send message to OpenAI's model and get response from it.
    """

    return await openai_service.chat(
        auth.user_id,
        api_key,
        chat_room_service,
        chat_history_service,
        payload,
    )

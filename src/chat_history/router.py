from uuid import UUID

from fastapi import APIRouter

from src.auth.dependencies import AuthDependency
from src.chat_room.dependencies import ChatRoomServiceDependency
from .dependencies import ChatHistoryServiceDependency


router = APIRouter(prefix="/chat-history", tags=["chat-history"])


@router.get("/{room_uuid}")
async def get_chat_history(
    room_uuid: UUID,
    auth: AuthDependency,
    chat_room_service: ChatRoomServiceDependency,
    chat_history_service: ChatHistoryServiceDependency,
):
    """
    Get the chat history of a specified chat room associated with the user.
    """

    return chat_history_service.get_user_chat_history(
        auth.user_id, room_uuid, chat_room_service
    )

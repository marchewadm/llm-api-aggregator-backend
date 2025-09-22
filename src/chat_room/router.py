import uuid

from fastapi import APIRouter

from src.auth.dependencies import AuthDependency
from .dependencies import ChatRoomServiceDependency

from .schemas import UserChatRoomsResponse


router = APIRouter(prefix="/chat-room", tags=["chat-room"])


@router.get("/all", response_model=UserChatRoomsResponse)
async def get_all_chat_rooms(
    auth: AuthDependency, chat_room_service: ChatRoomServiceDependency
):
    """
    Get all chat rooms associated with the user.
    """

    return chat_room_service.get_all_by_user_id(auth.user_id)


@router.delete("/{room_uuid}")
async def delete_chat_room(
    room_uuid: uuid.UUID,
    auth: AuthDependency,
    chat_room_service: ChatRoomServiceDependency,
):
    """
    Delete a chat room associated with the user by its UUID.
    """

    return chat_room_service.delete_chat_room(auth.user_id, room_uuid)

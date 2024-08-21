from fastapi import APIRouter

from src.auth.dependencies import AuthDependency
from .dependencies import ChatRoomServiceDependency


router = APIRouter(prefix="/chat-room", tags=["chat-room"])


@router.get("/all")
async def get_all_chat_rooms(
    auth: AuthDependency, chat_room_service: ChatRoomServiceDependency
):
    """
    Get all chat rooms.
    """

    return chat_room_service.get_all_by_user_id(auth.user_id)

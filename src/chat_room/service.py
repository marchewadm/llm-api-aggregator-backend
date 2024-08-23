import uuid

from fastapi import Depends, HTTPException, status

from src.shared.service.base import BaseService

from .repository import ChatRoomRepository
from .schemas import ChatRoom, UserChatRoomsResponse


class ChatRoomService(BaseService[ChatRoomRepository]):
    """
    Service for chat room related operations.
    """

    def __init__(
        self, repository: ChatRoomRepository = Depends(ChatRoomRepository)
    ) -> None:
        """
        Initializes the service with the repository.

        Args:
            repository (ChatRoomRepository): The repository to use for chat room operations.

        Returns:
            None
        """

        super().__init__(repository)

    def create(self, user_id: int) -> uuid.UUID:
        """
        Create a new chat room for a user and return the UUID of the chat room.

        Args:
            user_id (int): The user's ID.

        Returns:
            uuid.UUID: The UUID of the newly created chat room.
        """

        return self.repository.create({"user_id": user_id})

    def verify_chat_room_exists(self, user_id: int, room_uuid: str) -> None:
        """
        Verify if a chat room exists and belongs to a user.

        Args:
            user_id (int): The user's ID.
            room_uuid (str): The chat room's UUID.

        Raises:
            HTTPException: Raised with a 404 status code if the chat room does not exist or does not belong to the user.

        Returns:
            None
        """

        chat_room = (
            self.repository.get_one_with_selected_attributes_by_condition(
                ["user_id"],
                "room_uuid",
                room_uuid,
            )
        )

        if not chat_room or chat_room.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat room with the provided UUID does not belong to the user.",
            )

    def get_all_by_user_id(self, user_id: int) -> UserChatRoomsResponse:
        """
        Get all chat rooms associated with a user.

        Args:
            user_id (int): The user's ID.

        Returns:
            UserChatRoomsResponse: Response containing a list of chat rooms with the last message
            and the time it was sent.
        """

        chat_rooms = self.repository.get_all_by_user_id(user_id)

        if chat_rooms:
            chat_rooms = [
                ChatRoom(
                    room_uuid=chat_room.room_uuid,
                    last_message=chat_room.chat_history[-1].message,
                    last_message_sent_at=chat_room.chat_history[-1].sent_at,
                )
                for chat_room in chat_rooms
            ]

        return UserChatRoomsResponse(chat_rooms=chat_rooms)

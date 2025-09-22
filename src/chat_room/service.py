import uuid

from fastapi import Depends, HTTPException, status

from src.shared.service.base import BaseService
from src.shared.schemas import ChatHistoryCompletionRequest

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

    def verify_chat_room_exists(
        self, user_id: int, room_uuid: uuid.UUID
    ) -> None:
        """
        Verify if a chat room exists and belongs to a user.

        TODO: Consider using this method as a dependency.

        Args:
            user_id (int): The user's ID.
            room_uuid (uuid.UUID): The chat room's UUID.

        Raises:
            HTTPException: Raised with a 404 status code if the chat room does not exist or does not belong to the user.

        Returns:
            None
        """

        chat_room = (
            self.repository.get_one_with_selected_attributes_by_condition(
                ["user_id"],
                "room_uuid",
                str(room_uuid),
            )
        )

        if not chat_room or chat_room.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat room with the provided UUID does not belong to the user.",
            )

    def handle_room_uuid(
        self, user_id: int, payload: ChatHistoryCompletionRequest
    ) -> ChatHistoryCompletionRequest:
        """
        Handle the room UUID in the payload.

        Args:
            user_id (int): The ID of the user.
            payload (ChatHistoryCompletionRequest): The payload containing the chat history data.

        Returns:
            ChatHistoryCompletionRequest: The payload with the room UUID.
        """

        if not payload.room_uuid and len(payload.messages) == 1:
            chat_room_uuid = self.create(user_id)

            payload: ChatHistoryCompletionRequest = payload.model_copy(
                update={"room_uuid": chat_room_uuid}
            )
        else:
            self.verify_chat_room_exists(user_id, payload.room_uuid)

        return payload

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
                    api_provider_id=chat_room.chat_history[-1].api_provider_id,
                )
                for chat_room in chat_rooms
            ]

        return UserChatRoomsResponse(chat_rooms=chat_rooms)

    def delete_chat_room(self, user_id: int, room_uuid: uuid.UUID) -> None:
        """
        Delete a chat room associated with a user by its UUID.

        Args:
            user_id (int): The user's ID.
            room_uuid (uuid.UUID): The chat room's UUID.

        Returns:
            None
        """

        self.verify_chat_room_exists(user_id, room_uuid)
        self.repository.delete_by_id(room_uuid)

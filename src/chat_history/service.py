from uuid import UUID

from fastapi import Depends

from src.shared.service.base import BaseService
from src.shared.enums import RoleEnum
from src.shared.schemas import ChatHistoryCompletionRequest

from src.chat_room.dependencies import ChatRoomServiceDependency

from .repository import ChatHistoryRepository
from .schemas import (
    ChatHistoryMessage,
    ChatHistoryResponse,
    ChatHistoryInDb,
)


class ChatHistoryService(BaseService[ChatHistoryRepository]):
    """
    Service for chat history related operations.
    """

    def __init__(
        self, repository: ChatHistoryRepository = Depends(ChatHistoryRepository)
    ) -> None:
        """
        Initializes the service.

        Args:
            repository (ChatHistoryRepository): The repository to use for chat history operations.

        Returns:
            None
        """

        super().__init__(repository)

    def create(self, payload: ChatHistoryInDb) -> None:
        """
        Create a new chat history record in the database.

        Args:
            payload (ChatHistoryInDb): The payload containing the chat history data.

        Returns:
            None
        """

        self.repository.create(payload.model_dump())

    def get_user_chat_history(
        self,
        user_id: int,
        room_uuid: UUID,
        chat_room_service: ChatRoomServiceDependency,
    ) -> ChatHistoryResponse:
        """
        Get a user's chat history for a specific chat room.

        Args:
            user_id (int): The ID of the user.
            room_uuid (UUID): The UUID of the chat room.
            chat_room_service (ChatRoomServiceDependency): The chat room service dependency.

        Returns:
            ChatHistoryResponse: The chat history response object.
        """

        chat_room_service.verify_chat_room_exists(user_id, room_uuid)

        chat_histories = self.repository.get_chat_history_by_room_uuid(
            room_uuid
        )

        ai_model = chat_histories[-1].ai_model
        custom_instructions = chat_histories[-1].custom_instructions
        messages = [
            ChatHistoryMessage(
                message=chat_history.message,
                image_url=chat_history.image_url,
                role=chat_history.role,
                api_provider_id=(
                    chat_history.api_provider_id
                    if chat_history.role == RoleEnum.assistant
                    else None
                ),
                sent_at=chat_history.sent_at,
            )
            for chat_history in chat_histories
        ]

        return ChatHistoryResponse(
            room_uuid=room_uuid,
            ai_model=ai_model,
            custom_instructions=custom_instructions,
            messages=messages,
        )

    def store_chat_history(
        self,
        assistant_message: str,
        payload: ChatHistoryCompletionRequest,
    ) -> None:
        """
        Store the chat history for both the user and the assistant.

        Args:
            assistant_message (str): The message from the assistant.
            payload (ChatHistoryCompletionRequest): The payload containing the chat history data.

        Returns:
            None
        """

        def create_chat_history(
            role: RoleEnum, message: str, image_url: str | None = None
        ) -> ChatHistoryInDb:
            return ChatHistoryInDb(
                ai_model=payload.ai_model,
                role=role,
                room_uuid=payload.room_uuid,
                message=message,
                image_url=image_url,
                api_provider_id=payload.api_provider_id,
                custom_instructions=payload.custom_instructions,
            )

        user_chat_history = create_chat_history(
            RoleEnum.user,
            payload.messages[-1].message,
            payload.messages[-1].image_url,
        )
        assistant_chat_history = create_chat_history(
            RoleEnum.assistant, assistant_message
        )

        self.create(user_chat_history)
        self.create(assistant_chat_history)

from fastapi import Depends, HTTPException, status

from openai import OpenAI, AuthenticationError

from src.shared.service.base import BaseAiService

from src.auth.dependencies import AuthDependency
from src.redis.dependencies import RedisServiceDependency
from src.chat_room.dependencies import ChatRoomServiceDependency

from .repository import OpenAiRepository
from .schemas import (
    OpenAiChatCompletionRequest,
    OpenAiChatCompletionResponse,
    OpenAiChatHistoryInDb,
)


class OpenAiService(BaseAiService[OpenAiRepository]):
    """
    Service for OpenAI related operations.
    """

    def __init__(
        self, repository: OpenAiRepository = Depends(OpenAiRepository)
    ) -> None:
        """
        Initializes the service.

        Args:
            repository (OpenAiRepository): The repository to use for OpenAI operations.

        Returns:
            None
        """

        super().__init__(
            repository,
            [
                "gpt-4",
                "gpt-4-turbo",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-3.5-turbo",
            ],
        )

    def create(self, payload: OpenAiChatHistoryInDb) -> None:
        """
        Create a new OpenAI chat history record in the database.

        Args:
            payload (OpenAiChatHistoryInDb): The payload containing the chat history data.

        Returns:
            None
        """

        self.repository.create(payload.model_dump())

    @staticmethod
    async def get_api_key(
        auth: AuthDependency,
        redis_service: RedisServiceDependency,
        api_provider_name: str = "openai",
    ) -> str:
        """
        Retrieve an API key for a user based on the API provider name.

        Args:
            auth (AuthDependency): The authentication dependency.
            redis_service (RedisServiceDependency): The Redis service dependency.
            api_provider_name (str): The name of the API provider.

        Raises:
            HTTPException: Raised with status code 404 if the user does not have any API keys stored in Redis.

        Returns:
            str: The decrypted API key if found.
        """

        api_key = await redis_service.get_user_specific_api_key_from_cache(
            auth.uuid, api_provider_name
        )
        return api_key

    async def chat(
        self,
        user_id: int,
        api_key: str,
        payload: OpenAiChatCompletionRequest,
        chat_room_service: ChatRoomServiceDependency,
    ) -> OpenAiChatCompletionResponse:
        """
        Chat with OpenAI using the specified model.

        TODO: Handle more exceptions and edge cases.
        TODO: Store the chat history in Redis and PostgreSQL.
        TODO: Implement the chat history retrieval endpoint.
        TODO: Implement the chat history deletion endpoint.

        Args:
            user_id (int): The user's ID.
            api_key (str): The OpenAI API key.
            payload (OpenAiChatCompletionRequest): The payload containing the AI model name, optional custom
            instructions for the AI model and the message history containing the role and content.
            chat_room_service (ChatRoomServiceDependency): The chat room service dependency.

        Raises:
            HTTPException: Raised with status code 400 if the AI model name is invalid.
            HTTPException: Raised with status code 401 if the OpenAI API key is invalid.

        Returns:
            OpenAiChatCompletionResponse: The response containing AI model's message and timestamp.
        """

        if not payload.room_uuid and len(payload.messages) == 1:
            chat_room_uuid = chat_room_service.create(user_id)

            payload: OpenAiChatCompletionRequest = payload.model_copy(
                update={"room_uuid": chat_room_uuid}
            )
        else:
            chat_room_service.verify_chat_room_exists(
                user_id, payload.room_uuid
            )

        try:
            client: OpenAI = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model=payload.ai_model,
                messages=[
                    {
                        "role": "system",
                        "content": payload.custom_instructions,
                    },
                    *payload.messages,
                ],
            )

            user_chat_history = OpenAiChatHistoryInDb(
                room_uuid=payload.room_uuid,
                message=payload.messages[-1].content,
                role="user",
                ai_model=payload.ai_model,
                custom_instructions=payload.custom_instructions,
            )
            assistant_chat_history = OpenAiChatHistoryInDb(
                room_uuid=payload.room_uuid,
                message=response.choices[0].message.content,
                role="assistant",
                ai_model=payload.ai_model,
                custom_instructions=payload.custom_instructions,
            )

            self.create(user_chat_history)
            self.create(assistant_chat_history)

            return OpenAiChatCompletionResponse(
                room_uuid=payload.room_uuid,
                response_message=response.choices[0].message.content,
            )
        except AuthenticationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OpenAI API key.",
            )

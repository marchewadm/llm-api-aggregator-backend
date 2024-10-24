from fastapi import HTTPException, status

from openai import OpenAI, AuthenticationError

from src.shared.service.base import BaseAiService

from src.auth.dependencies import AuthDependency
from src.redis.dependencies import RedisServiceDependency
from src.chat_room.dependencies import ChatRoomServiceDependency
from src.chat_history.dependencies import ChatHistoryServiceDependency

from src.shared.schemas import (
    ChatHistoryCompletionRequest,
    ChatHistoryCompletionResponse,
)


class OpenAiService(BaseAiService):
    """
    Service for OpenAI related operations.
    """

    def __init__(self) -> None:
        """
        Initializes the service.

        Returns:
            None
        """

        super().__init__()

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

    @staticmethod
    async def chat(
        user_id: int,
        api_key: str,
        chat_room_service: ChatRoomServiceDependency,
        chat_history_service: ChatHistoryServiceDependency,
        payload: ChatHistoryCompletionRequest,
    ):
        """
        TODO: Handle more exceptions and edge cases.
        TODO: Store the chat history in Redis

        Send message to OpenAI's model, get response from it, store the chat history and return the response.

        Args:
            user_id (int): The user's ID.
            api_key (str): The OpenAI API key.
            chat_room_service (ChatRoomServiceDependency): The chat room service dependency.
            chat_history_service (ChatHistoryServiceDependency): The chat history service dependency.
            payload (ChatHistoryCompletionRequest): The payload containing the AI model name, optional custom
            instructions for the AI model and the message history containing the role and content.

        Raises:
            HTTPException: Raised with status code 401 if the OpenAI API key is invalid.

        Returns:
            ChatHistoryCompletionResponse: The response containing AI model's message and room UUID.
        """

        payload = chat_room_service.handle_room_uuid(user_id, payload)

        try:
            client: OpenAI = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model=payload.ai_model,
                messages=[
                    {
                        "role": "system",
                        "content": payload.custom_instructions,
                    },
                    *[
                        {
                            "role": msg_payload.role,
                            "content": msg_payload.message,
                        }
                        for msg_payload in payload.messages
                    ],
                ],
            )

            chat_history_service.store_chat_history(
                response.choices[0].message.content, payload
            )

            return ChatHistoryCompletionResponse(
                message=response.choices[0].message.content,
                room_uuid=payload.room_uuid,
                api_provider_id=payload.api_provider_id,
            )
        except AuthenticationError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid OpenAI API key.",
            )

from fastapi import HTTPException, status, UploadFile

from openai import OpenAI, AuthenticationError, NotFoundError, OpenAIError

from src.shared.service.base import BaseAiService

from src.auth.dependencies import AuthDependency
from src.redis.dependencies import RedisServiceDependency
from src.chat_room.dependencies import ChatRoomServiceDependency
from src.chat_history.dependencies import ChatHistoryServiceDependency
from src.s3.dependencies import S3ServiceDependency

from src.shared.schemas import (
    ChatHistoryCompletionRequest,
    ChatHistoryCompletionResponse,
    ChatHistoryUploadImageResponse,
    ChatHistoryCompletionMessage,
)


class OpenAiService(BaseAiService):
    """
    Service for OpenAI related operations.
    """

    def __init__(self, s3_service: S3ServiceDependency) -> None:
        """
        Initializes the service.

        Returns:
            None
        """

        super().__init__()
        self.s3_service = s3_service

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

    async def upload_image(
        self, image: UploadFile
    ) -> ChatHistoryUploadImageResponse:
        """
        Upload an image to S3 and return the URL to use it in the chat message.

        Args:
            image (UploadFile): The image file to upload.

        Returns:
            ChatHistoryUploadImageResponse: The response containing the image URL.
        """

        image_url = await self.s3_service.upload_file(image, "openai-images")
        return ChatHistoryUploadImageResponse(image_url=image_url)

    async def chat(
        self,
        user_id: int,
        api_key: str,
        chat_room_service: ChatRoomServiceDependency,
        chat_history_service: ChatHistoryServiceDependency,
        payload: ChatHistoryCompletionRequest,
    ) -> ChatHistoryCompletionResponse:
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
            HTTPException: Raised with status code 403 if the OpenAI API key is invalid.

        Returns:
            ChatHistoryCompletionResponse: The response containing AI model's message and room UUID.
        """

        try:
            client: OpenAI = OpenAI(api_key=api_key)

            messages = self._format_messages(payload.messages)

            response = client.chat.completions.create(
                model=payload.ai_model,
                messages=[
                    {
                        "role": "system",
                        "content": payload.custom_instructions,
                    },
                    *messages,
                ],
            )

            payload = chat_room_service.handle_room_uuid(user_id, payload)

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
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="OpenAI model not found.",
            )
        except OpenAIError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong with OpenAI API. Please try again later.",
            )

    @staticmethod
    def _format_messages(
        messages: list[ChatHistoryCompletionMessage],
    ) -> list[dict]:
        """
        Format the messages to be sent to OpenAI's API.

        Args:
            messages (list[ChatHistoryCompletionMessage]): The list of messages to be formatted.

        Returns:
            list[dict]: The formatted messages.
        """

        formatted_messages = []

        for msg in messages:
            message_parts = [{"type": "text", "text": msg.message}]

            if msg.image_url:
                message_parts.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": msg.image_url},
                    }
                )

            formatted_messages.append(
                {
                    "role": msg.role,
                    "content": message_parts,
                }
            )

        return formatted_messages

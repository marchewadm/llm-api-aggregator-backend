from fastapi import status, HTTPException, UploadFile

from google import generativeai as genai
from google.generativeai.types import File
from google.api_core.exceptions import (
    InvalidArgument,
    NotFound,
    PermissionDenied,
)

from src.shared.service.base import BaseAiService

from src.auth.dependencies import AuthDependency
from src.redis.dependencies import RedisServiceDependency
from src.chat_room.dependencies import ChatRoomServiceDependency
from src.chat_history.dependencies import ChatHistoryServiceDependency
from src.s3.dependencies import S3ServiceDependency

from src.shared.enums import RoleEnum
from src.shared.schemas import (
    ChatHistoryCompletionRequest,
    ChatHistoryCompletionResponse,
    ChatHistoryUploadImageResponse,
    ChatHistoryCompletionMessage,
)


class GeminiService(BaseAiService):
    """
    Service for Google Gemini related operations.
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
        api_provider_name: str = "gemini",
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

        image_url = await self.s3_service.upload_file(image, "gemini-images")
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
        Send message to Google Gemini's model, get response from it, store the chat history and return the response.

        Args:
            user_id (int): The user's ID.
            api_key (str): The Gemini API key.
            chat_room_service (ChatRoomServiceDependency): The chat room service dependency.
            chat_history_service (ChatHistoryServiceDependency): The chat history service dependency.
            payload (ChatHistoryCompletionRequest): The request payload containing the AI model name, optional custom
             instructions for the AI model and the message history containing the role and content.

        Raises:
            HTTPException: Raised with status code 403 if the Gemini API key is invalid.

        Returns:
            ChatHistoryCompletionResponse: The response containing room UUID, messages, API provider ID
             with AI model name and its custom instructions.
        """

        try:
            genai.configure(api_key=api_key)

            model = genai.GenerativeModel(
                model_name=payload.ai_model,
                system_instruction=payload.custom_instructions,
            )

            response = await model.generate_content_async(
                self._format_messages(payload.messages)
            )

            payload = chat_room_service.handle_room_uuid(user_id, payload)
            chat_history_service.store_chat_history(response.text, payload)

            return ChatHistoryCompletionResponse(
                message=response.text,
                room_uuid=payload.room_uuid,
                api_provider_id=payload.api_provider_id,
            )
        except InvalidArgument as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Invalid Gemini API key: {e}",
            )
        except NotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gemini model not found.",
            )

    def _format_messages(
        self,
        messages: list[ChatHistoryCompletionMessage],
    ) -> list[dict]:
        """
        Format the messages to be sent to Gemini's API.

        Args:
            messages (list[ChatHistoryCompletionMessage]): The list of messages to format.

        Returns:
            list[dict]: The formatted messages.
        """

        formatted_messages = []

        for msg in messages:
            role = msg.role if msg.role == RoleEnum.user else "model"
            message_parts: dict[str, list[str | File]] = {
                "role": role,
                "parts": [msg.message],
            }

            if msg.image_url:
                clean_filename = self.s3_service.get_clean_filename_from_url(
                    msg.image_url
                )

                try:
                    image_file = genai.get_file(clean_filename)
                except PermissionDenied:
                    s3_key = self.s3_service.extract_s3_key_from_url(
                        msg.image_url
                    )
                    local_path = self.s3_service.download_file_to_local(s3_key)
                    image_file = genai.upload_file(
                        path=local_path, name=clean_filename
                    )
                    self.s3_service.delete_local_file(local_path)

                message_parts["parts"].append(image_file)

            formatted_messages.append(message_parts)

        return formatted_messages

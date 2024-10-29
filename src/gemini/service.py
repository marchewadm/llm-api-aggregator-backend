from fastapi import status, HTTPException

from google import generativeai as genai
from google.api_core.exceptions import InvalidArgument, NotFound

from src.shared.service.base import BaseAiService

from src.auth.dependencies import AuthDependency
from src.redis.dependencies import RedisServiceDependency
from src.chat_room.dependencies import ChatRoomServiceDependency
from src.chat_history.dependencies import ChatHistoryServiceDependency

from src.shared.schemas import (
    ChatHistoryCompletionRequest,
    ChatHistoryCompletionResponse,
)


class GeminiService(BaseAiService):
    """
    Service for Google Gemini related operations.
    """

    def __init__(self):
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

    @staticmethod
    async def chat(
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

            chat = model.start_chat(
                history=[
                    *[
                        {
                            "role": (
                                "user"
                                if msg_payload.role == "user"
                                else "model"
                            ),
                            "parts": msg_payload.message,
                        }
                        # Exclude the last message because Gemini API uses it in the next line to perform the request
                        for msg_payload in payload.messages[:-1]
                    ]
                ]
            )
            response = await chat.send_message_async(
                payload.messages[-1].message
            )

            payload = chat_room_service.handle_room_uuid(user_id, payload)
            chat_history_service.store_chat_history(response.text, payload)

            return ChatHistoryCompletionResponse(
                message=response.text,
                room_uuid=payload.room_uuid,
                api_provider_id=payload.api_provider_id,
            )
        except InvalidArgument:
            # Gemini throws InvalidArgument when the API key is invalid
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Gemini API key.",
            )
        except NotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gemini model not found.",
            )

from fastapi import Depends, HTTPException, status

from openai import OpenAI, AuthenticationError

from src.shared.service.base import BaseAiService

from src.auth.dependencies import AuthDependency
from src.redis.dependencies import RedisServiceDependency

from .repository import OpenAiRepository
from .schemas import OpenAiChatCompletionRequest, OpenAiChatCompletionResponse


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

    def create(self, payload) -> None:
        pass

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
        api_key: str, payload: OpenAiChatCompletionRequest
    ) -> OpenAiChatCompletionResponse:
        """
        Chat with OpenAI using the specified model.

        Args:
            api_key (str): The OpenAI API key.
            payload (OpenAiChatCompletionRequest): The payload containing the AI model name, optional custom
            instructions for the AI model and the message history containing the role and content.

        Raises:
            HTTPException: Raised with status code 400 if the AI model name is invalid.
            HTTPException: Raised with status code 401 if the OpenAI API key is invalid.

        Returns:
            OpenAiChatCompletionResponse: The response containing AI model's message and timestamp.
        """

        try:
            client: OpenAI = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model=payload.ai_model,
                messages=[
                    {
                        "role": "system",
                        "content": payload.custom_instructions,
                    },
                    *payload.get_sorted_messages(),
                ],
            )

            # TODO: Store the chat history in Redis and PostgreSQL.
            # TODO: Implement the chat history retrieval endpoint.
            # TODO: Implement the chat history deletion endpoint.
            # TODO: Implement the chat history update endpoint.
            # TODO: Implement missing created_at field in OpenAiChatCompletionResponse.

            return OpenAiChatCompletionResponse(
                response_message=response.choices[0].message.content,
            )
        except AuthenticationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OpenAI API key.",
            )

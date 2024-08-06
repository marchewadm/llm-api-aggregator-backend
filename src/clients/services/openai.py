from fastapi import HTTPException, status

from openai import OpenAI, AuthenticationError

from src.clients.schemas.openai import (
    OpenAiChatCompletionRequest,
    OpenAiChatCompletionResponse,
)

from .base import BaseService


class OpenAiService(BaseService):
    """
    Service for OpenAI related operations.
    """

    def __init__(self) -> None:
        """
        Initializes the service.

        Returns:
            None
        """

        super().__init__(
            ai_models=[
                "gpt-4",
                "gpt-4-turbo",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-3.5-turbo",
            ]
        )

    @classmethod
    def _get_api_provider_name(cls) -> str:
        """
        The name of the API provider.

        Returns:
            str: The name of the API provider.
        """

        return "openai"

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

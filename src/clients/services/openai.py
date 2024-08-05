from fastapi import HTTPException, status

from openai import OpenAI, AuthenticationError

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

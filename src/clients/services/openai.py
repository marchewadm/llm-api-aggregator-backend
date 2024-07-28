from fastapi import HTTPException, status

from openai import OpenAI, AuthenticationError

from .base import BaseService


class OpenAiService(BaseService):
    """
    Service for OpenAI related operations.
    """

    @classmethod
    def _get_api_provider_name(cls) -> str:
        """
        The name of the API provider.

        Returns:
            str: The name of the API provider.
        """

        return "openai"

    @staticmethod
    async def get_models(api_key: str) -> dict:
        """
        Get all available OpenAI models for the user.

        Args:
            api_key (str): The OpenAI API key retrieved from Redis cache.

        Returns:
            dict: The available OpenAI models.
        """

        try:
            client = OpenAI(api_key=api_key)
            return client.models.list()
        except AuthenticationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OpenAI API key.",
            )

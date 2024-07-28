from .base import BaseService


class OpenAiService(BaseService):
    """
    Service for OpenAI related operations.
    """

    @classmethod
    def _get_api_provider_name(cls) -> str:
        """
        The name of the API provider.
        """

        return "openai"

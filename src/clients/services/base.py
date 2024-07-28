from abc import ABC, abstractmethod

from src.dependencies import AuthDependency, RedisServiceDependency


class BaseService(ABC):
    """
    Base class for external APIs services.
    """

    def __init__(self) -> None:
        """
        Initializes the service.
        """

    @classmethod
    @abstractmethod
    def _get_api_provider_name(cls) -> str:
        """
        The name of the API provider.
        """

        pass

    @classmethod
    async def get_api_key(
        cls,
        auth: AuthDependency,
        redis_service: RedisServiceDependency,
    ) -> str:
        """
        Retrieve an API key for a user based on the API provider name.

        Args:
            auth (AuthDependency): The authentication dependency.
            redis_service (RedisServiceDependency): The Redis service dependency.

        Raises:
            HTTPException: Raised with status code 404 if the user does not have any API keys stored in Redis.

        Returns:
            str: The decrypted API key if found.
        """

        api_key = await redis_service.get_user_specific_api_key_from_cache(
            auth.uuid, cls._get_api_provider_name()
        )

        return api_key

from cryptography.fernet import Fernet

from fastapi import Depends

from src.repositories.api_key import ApiKeyRepository
from src.schemas.api_key import ApiKey, ApiKeysResponse

from .base import BaseService


class ApiKeyService(BaseService[ApiKeyRepository]):
    """
    Service for API key related operations.
    """

    def __init__(
        self, repository: ApiKeyRepository = Depends(ApiKeyRepository)
    ) -> None:
        """
        Initializes the service with the repository.

        Args:
            repository (ApiKeyRepository): The repository to use for API key operations.

        Returns:
            None
        """

        super().__init__(repository)

    def create(self, payload) -> None:
        """
        This method is implemented in AuthService, but not in ApiKeyService.
        """

        pass

    def get_user_api_keys(
        self, user_id: int, fernet_key: Fernet
    ) -> ApiKeysResponse:
        """
        Get all user's API keys by user ID and decrypt them using the user's Fernet key.

        Args:
            user_id (int): The user's ID.
            fernet_key (bytes): The user's Fernet key.

        Returns:
            ApiKeysResponse: The API keys response containing the user's API keys.
        """

        api_keys = self.repository.get_all_by_user_id(user_id)

        if api_keys:
            api_keys = [
                ApiKey(
                    key=fernet_key.decrypt(api_key.key).decode(),
                    api_provider_name=api_key.api_provider.name,
                    api_provider_lowercase_name=api_key.api_provider.lowercase_name,
                )
                for api_key in api_keys
            ]

        return ApiKeysResponse(api_keys=api_keys)

    def delete_user_api_keys(self, user_id: int) -> None:
        """
        Delete all API keys associated with the user by their ID.

        Args:
            user_id (int): The user's ID.

        Returns:
            None
        """

        self.repository.delete_all_by_user_id(user_id)

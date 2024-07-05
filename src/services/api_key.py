from cryptography.fernet import Fernet

from fastapi import Depends, HTTPException, status

from src.repositories.api_key import ApiKeyRepository
from src.schemas.api_key import (
    ApiKey,
    ApiKeysResponse,
    ApiKeysUpdate,
    ApiKeysUpdateResponse,
)

from src.schemas.api_provider import ApiProvidersResponse

from src.utils.passphrase import passphrase_util

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
                    key=fernet_key.decrypt(
                        passphrase_util.convert_hex_to_bytes(api_key.key)
                    ),
                    api_provider_id=api_key.api_provider.id,
                    api_provider_name=api_key.api_provider.name,
                    api_provider_lowercase_name=api_key.api_provider.lowercase_name,
                )
                for api_key in api_keys
            ]

        return ApiKeysResponse(api_keys=api_keys)

    def update_user_api_keys(
        self,
        user_id: int,
        fernet_key: Fernet,
        payload: ApiKeysUpdate,
        api_providers: ApiProvidersResponse,
    ) -> ApiKeysUpdateResponse:
        """
        Update the user's API keys in the database based on the user's ID.

        Args:
            user_id (int): The user's ID.
            fernet_key (Fernet): The user's Fernet key to encrypt the API keys.
            payload (ApiKeysUpdate): The payload containing the passphrase and the API keys.
            api_providers (ApiProvidersResponse): The API providers response containing the API providers.

        Returns:
            ApiKeysUpdateResponse: The result of the operation containing a message.
        """

        # user2@example.com
        # b|uz$`G)tL7c_pbs}E9g5_HY0nVug~y54F?TcP{Y>sOJ`s8)%$Rf;s~X5&b+n*|8zwIe,wQGos4p#.OAjg8@r!o?qrJL])Cmo2W$/?LRYd@G?-Uam>{T@ya`Wi<uW`,g

        db_api_keys = self.get_user_api_keys(user_id, fernet_key).model_dump()
        api_providers = api_providers.model_dump()
        print(db_api_keys)

        api_keys_to_update: list[dict] = []
        api_keys_to_create: list[dict] = []
        api_keys_to_delete: list[dict] = []

        is_updated: bool = False
        is_created: bool = False
        is_deleted: bool = False

        for db_api_key in db_api_keys["api_keys"]:
            api_key_exists = any(
                db_api_key["api_provider_id"] == api_key.api_provider_id
                for api_key in payload.api_keys
            )
            if not api_key_exists:
                api_keys_to_delete.append(
                    {
                        "api_provider_id": db_api_key["api_provider_id"],
                    }
                )
                is_deleted = True

        for api_key in payload.api_keys:
            api_provider_exists = any(
                api_provider["id"] == api_key.api_provider_id
                for api_provider in api_providers["api_providers"]
            )

            if not api_provider_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid API provider ID.",
                )

            different_key_exists = any(
                item["api_provider_id"] == api_key.api_provider_id
                and item["key"] != api_key.key
                for item in db_api_keys["api_keys"]
            )
            same_key_exists = any(
                item["api_provider_id"] == api_key.api_provider_id
                and item["key"] == api_key.key
                for item in db_api_keys["api_keys"]
            )

            if different_key_exists:
                api_keys_to_update.append(
                    {
                        "key": passphrase_util.convert_bytes_to_hex(
                            fernet_key.encrypt(api_key.key.encode())
                        ),
                        "api_provider_id": api_key.api_provider_id,
                    }
                )
                is_updated = True
            elif not same_key_exists:
                api_keys_to_create.append(
                    {
                        "key": passphrase_util.convert_bytes_to_hex(
                            fernet_key.encrypt(api_key.key.encode())
                        ),
                        "user_id": user_id,
                        "api_provider_id": api_key.api_provider_id,
                    }
                )
                is_created = True

        if is_updated:
            self.repository.update_bulk_by_user_id(user_id, api_keys_to_update)
        if is_created:
            self.repository.create_bulk(api_keys_to_create)
        if is_deleted:
            self.repository.delete_selected_by_user_id(
                user_id, api_keys_to_delete
            )

        if is_updated or is_created or is_deleted:
            return ApiKeysUpdateResponse(
                message="API keys updated successfully."
            )
        else:
            return ApiKeysUpdateResponse(
                message="Your API keys are already up to date. No changes were made."
            )

    def delete_user_api_keys(self, user_id: int) -> None:
        """
        Delete all API keys associated with the user by their ID.

        Args:
            user_id (int): The user's ID.

        Returns:
            None
        """

        self.repository.delete_all_by_user_id(user_id)

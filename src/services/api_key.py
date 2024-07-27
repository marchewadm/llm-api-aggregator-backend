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
                    id=api_key.id,
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

    def _set_api_key_operation(
        self,
        user_id: int,
        fernet_key: Fernet,
        db_all_api_providers: ApiProvidersResponse,
        payload: ApiKeysUpdate,
    ) -> tuple[list[dict], list[dict], list[dict]]:
        """
        Helper method to set the API key CRUD operation based on the payload.

        Args:
            user_id (int): The user's ID.
            fernet_key (Fernet): The user's Fernet key.
            db_all_api_providers (ApiProvidersResponse): All API providers.
            payload (ApiKeysUpdate): The API keys update payload.

        Returns:
            tuple[list[dict], list[dict], list[dict]]: A tuple containing the API keys to create, update and delete.
        """

        db_api_keys = self.get_user_api_keys(user_id, fernet_key)

        api_keys_to_create: list[dict] = []
        api_keys_to_update: list[dict] = []
        api_keys_to_delete: list[dict] = []

        payload_provider_ids: set[int] = {
            api_key.api_provider_id for api_key in payload.api_keys
        }
        db_provider_ids: set[int] = {
            provider.id for provider in db_all_api_providers.api_providers
        }
        invalid_provider_ids: set[int] = payload_provider_ids - db_provider_ids

        if invalid_provider_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid API provider ID(s): {', '.join(map(str, invalid_provider_ids))}",
            )

        api_keys_to_delete = [
            {"id": db_api_key.id}
            for db_api_key in db_api_keys.api_keys
            if db_api_key.api_provider_id not in payload_provider_ids
        ]

        for api_key in payload.api_keys:
            encrypted_key = passphrase_util.convert_bytes_to_hex(
                fernet_key.encrypt(api_key.key.encode())
            )

            existing_key = next(
                (
                    db_api_key
                    for db_api_key in db_api_keys.api_keys
                    if db_api_key.api_provider_id == api_key.api_provider_id
                ),
                None,
            )

            if existing_key:
                if existing_key.key != api_key.key:
                    api_keys_to_update.append(
                        {
                            "id": existing_key.id,
                            "key": encrypted_key,
                        }
                    )
            else:
                api_keys_to_create.append(
                    {
                        "key": encrypted_key,
                        "user_id": user_id,
                        "api_provider_id": api_key.api_provider_id,
                    }
                )

        return api_keys_to_create, api_keys_to_update, api_keys_to_delete

    def update_user_api_keys(
        self,
        user_id: int,
        fernet_key: Fernet,
        db_all_api_providers: ApiProvidersResponse,
        payload: ApiKeysUpdate,
    ) -> ApiKeysUpdateResponse:
        """
        Update the user's API keys in the database based on the user's ID.

        Args:
            user_id (int): The user's ID.
            fernet_key (Fernet): The user's Fernet key.
            db_all_api_providers (ApiProvidersResponse): All API providers.
            payload (ApiKeysUpdate): The API keys update payload.

        Returns:
            ApiKeysUpdateResponse: The API keys update response containing the message.
        """

        api_keys_to_create, api_keys_to_update, api_keys_to_delete = (
            self._set_api_key_operation(
                user_id, fernet_key, db_all_api_providers, payload
            )
        )

        if api_keys_to_create or api_keys_to_update or api_keys_to_delete:
            if api_keys_to_create:
                self.repository.create_bulk(api_keys_to_create)
            if api_keys_to_update:
                self.repository.update_bulk(api_keys_to_update)
            if api_keys_to_delete:
                self.repository.delete_selected_by_user_id(
                    user_id, api_keys_to_delete
                )

            return ApiKeysUpdateResponse(
                message="API keys updated successfully.",
                is_updated=True,
            )
        else:
            return ApiKeysUpdateResponse(
                message="Your API keys are already up to date. No changes were made.",
                is_updated=False,
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

from fastapi import APIRouter

from src.dependencies import (
    AuthDependency,
    AuthServiceDependency,
    ApiKeyServiceDependency,
    ApiProviderServiceDependency,
)

from src.schemas.api_key import (
    ApiKeysResponse,
    ApiKeysPassphrase,
    ApiKeysUpdate,
    ApiKeysUpdateResponse,
)


router = APIRouter(prefix="/api-key", tags=["api-key"])


@router.post("", response_model=ApiKeysResponse)
async def get_api_keys(
    auth: AuthDependency,
    auth_service: AuthServiceDependency,
    api_key_service: ApiKeyServiceDependency,
    payload: ApiKeysPassphrase,
):
    """
    Verify the user's passphrase and retrieve all user's API keys from the database based on the user's ID.
    """

    fernet_key = auth_service.get_fernet_key(
        auth.user_id, payload.passphrase.get_secret_value()
    )

    return api_key_service.get_user_api_keys(auth.user_id, fernet_key)


@router.patch("", response_model=ApiKeysUpdateResponse)
async def update_api_keys(
    auth: AuthDependency,
    auth_service: AuthServiceDependency,
    api_key_service: ApiKeyServiceDependency,
    api_provider_service: ApiProviderServiceDependency,
    payload: ApiKeysUpdate,
):
    """
    Update the user's API keys in the database based on the user's ID.
    """

    fernet_key = auth_service.get_fernet_key(
        auth.user_id, payload.passphrase.get_secret_value()
    )

    api_providers = api_provider_service.get_all()

    return api_key_service.update_user_api_keys(
        auth.user_id, fernet_key, payload, api_providers
    )

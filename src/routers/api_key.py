from fastapi import APIRouter

from src.dependencies import (
    AuthDependency,
    AuthServiceDependency,
    ApiKeyServiceDependency,
    ApiProviderServiceDependency,
    RedisServiceDependency,
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
    redis_service: RedisServiceDependency,
    payload: ApiKeysPassphrase,
):
    """
    Verify the user's passphrase and retrieve all user's API keys from the database based on the user's ID.
    """

    fernet_key = auth_service.get_fernet_key(
        auth.user_id, payload.passphrase.get_secret_value()
    )

    user_api_keys = api_key_service.get_user_api_keys(auth.user_id, fernet_key)

    await redis_service.set_user_api_keys_in_cache(auth.uuid, user_api_keys)

    return user_api_keys


@router.patch("", response_model=ApiKeysUpdateResponse)
async def update_api_keys(
    auth: AuthDependency,
    auth_service: AuthServiceDependency,
    api_key_service: ApiKeyServiceDependency,
    api_provider_service: ApiProviderServiceDependency,
    redis_service: RedisServiceDependency,
    payload: ApiKeysUpdate,
):
    """
    Update the user's API keys in the database based on the user's ID.
    """

    fernet_key = auth_service.get_fernet_key(
        auth.user_id, payload.passphrase.get_secret_value()
    )

    db_all_api_providers = api_provider_service.get_all()

    updated_user_api_keys = api_key_service.update_user_api_keys(
        auth.user_id, fernet_key, db_all_api_providers, payload
    )

    if updated_user_api_keys.is_updated:
        user_api_keys = api_key_service.get_user_api_keys(
            auth.user_id, fernet_key
        )
        await redis_service.set_user_api_keys_in_cache(auth.uuid, user_api_keys)

    return updated_user_api_keys

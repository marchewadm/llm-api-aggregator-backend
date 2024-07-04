from fastapi import APIRouter

from src.dependencies import (
    AuthDependency,
    AuthServiceDependency,
    ApiKeyServiceDependency,
)

from src.schemas.api_key import ApiKeysResponse
from src.schemas.auth import AuthPassphrase


router = APIRouter(prefix="/api-key", tags=["api-key"])


@router.post("", response_model=ApiKeysResponse)
async def get_api_keys(
    auth: AuthDependency,
    auth_service: AuthServiceDependency,
    api_key_service: ApiKeyServiceDependency,
    payload: AuthPassphrase,
):
    """
    Verify the user's passphrase and retrieve all user's API keys from the database based on the user's ID.
    """

    fernet_key = auth_service.get_fernet_key(
        auth.user_id, payload.passphrase.get_secret_value()
    )

    return api_key_service.get_user_api_keys(auth.user_id, fernet_key)

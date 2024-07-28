from fastapi import APIRouter

from src.dependencies import (
    AuthDependency,
    UserServiceDependency,
    ApiKeyServiceDependency,
    RedisServiceDependency,
)
from src.schemas.user import (
    UserUpdatePassword,
    UserUpdateProfile,
    UserProfileResponse,
    UserUpdatePasswordResponse,
    UserUpdateProfileResponse,
    UserUpdatePassphraseResponse,
)


router = APIRouter(prefix="/user", tags=["user"])


@router.get("", response_model=UserProfileResponse)
async def get_user_profile(
    auth: AuthDependency,
    user_service: UserServiceDependency,
):
    """
    Get the user's profile by user ID.
    """

    return user_service.get_profile(auth.user_id)


@router.patch("/update-password", response_model=UserUpdatePasswordResponse)
async def update_user_password(
    auth: AuthDependency,
    user_service: UserServiceDependency,
    payload: UserUpdatePassword,
):
    """
    Update the user's password by user ID.
    """

    return user_service.update_user_password(auth.user_id, payload)


@router.patch("/update-profile", response_model=UserUpdateProfileResponse)
async def update_user_profile(
    auth: AuthDependency,
    user_service: UserServiceDependency,
    payload: UserUpdateProfile,
):
    """
    Update the user's profile by user ID.
    """

    return user_service.update_user_profile(auth.user_id, payload)


@router.patch("/update-passphrase", response_model=UserUpdatePassphraseResponse)
async def update_user_passphrase(
    auth: AuthDependency,
    user_service: UserServiceDependency,
    api_key_service: ApiKeyServiceDependency,
    redis_service: RedisServiceDependency,
):
    """
    Update the user's passphrase by user ID, delete all API keys associated with the user and return a strong, random
    generated passphrase for the user so that they can save it in a secure place.
    """

    passphrase = user_service.update_user_passphrase(auth.user_id)

    api_key_service.delete_user_api_keys(auth.user_id)
    await redis_service.delete_user_api_keys_from_cache(auth.uuid)

    return passphrase

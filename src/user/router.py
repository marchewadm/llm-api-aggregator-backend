from typing import Annotated

from fastapi import APIRouter, Form, UploadFile

from src.auth.dependencies import AuthDependency
from src.api_key.dependencies import ApiKeyServiceDependency
from src.redis.dependencies import RedisServiceDependency
from .dependencies import UserServiceDependency

from .schemas import (
    UserUpdatePasswordRequest,
    UserUpdateProfileRequest,
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
    payload: UserUpdatePasswordRequest,
):
    """
    Update the user's password by user ID.
    """

    return user_service.update_user_password(auth.user_id, payload)


# TODO: Validate image file
# TODO: Add a global rate limiter and especially for this endpoint make it lower due to the file upload
@router.patch("/update-profile", response_model=UserUpdateProfileResponse)
async def update_user_profile(
    auth: AuthDependency,
    user_service: UserServiceDependency,
    payload: Annotated[UserUpdateProfileRequest, Form()],
    avatar: UploadFile | None = None,
):
    """
    Update the user's profile by user ID.
    """

    return await user_service.update_user_profile(auth.user_id, payload, avatar)


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

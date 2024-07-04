from fastapi import APIRouter

from src.dependencies import AuthDependency, UserServiceDependency
from src.schemas.user import (
    UserUpdatePassword,
    UserUpdateProfile,
    UserProfileResponse,
    UserUpdatePasswordResponse,
    UserUpdateProfileResponse,
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

from fastapi import APIRouter

from src.dependencies import AuthDependency, UserServiceDependency
from src.schemas.user import UserProfileResponse, UserUpdatePassword


router = APIRouter(prefix="/user", tags=["user"])


@router.get("", response_model=UserProfileResponse)
async def get_user_profile(
    auth: AuthDependency,
    user_service: UserServiceDependency,
):
    return user_service.get_user_profile(auth.user_id)


@router.patch("/update-password")
async def update_user_password(
    auth: AuthDependency,
    user_service: UserServiceDependency,
    payload: UserUpdatePassword,
):
    return user_service.update_user_password(auth.user_id, payload)

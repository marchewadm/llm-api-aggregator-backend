from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies import UserServiceDependency, AuthDependency

from .schemas import (
    UserLoginResponse,
    UserRegister,
    UserRegisterResponse,
    UserProfileResponse,
)


auth_router = APIRouter(prefix="/auth", tags=["auth"])
user_router = APIRouter(prefix="/user", tags=["user"])


@auth_router.post("/login", response_model=UserLoginResponse)
async def login_user(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDependency,
):
    result = user_service.authenticate_user(payload)
    return result


@auth_router.post("/register", response_model=UserRegisterResponse)
async def register_user(
    payload: UserRegister, user_service: UserServiceDependency
):
    result = user_service.create_user(payload)
    return result


@user_router.get("", response_model=UserProfileResponse)
async def get_user_profile(
    auth: AuthDependency, user_service: UserServiceDependency
):
    result = user_service.get_user_profile(auth.user_id)
    return result

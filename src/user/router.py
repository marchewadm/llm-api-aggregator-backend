from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies import UserServiceDependency

from .schemas import (
    UserLoginResponse,
    UserRegister,
    UserRegisterResponse,
)


auth_router = APIRouter(prefix="/auth", tags=["auth"])
user_router = APIRouter(prefix="/user", tags=["user"])


@auth_router.post("/login", response_model=UserLoginResponse)
async def login_user(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDependency,
):
    result = user_service.authenticate(payload)
    return result


@auth_router.post("/register", response_model=UserRegisterResponse)
async def register_user(
    payload: UserRegister, user_service: UserServiceDependency
):
    result = user_service.create(payload)
    return result

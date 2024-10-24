from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .dependencies import AuthServiceDependency
from .schemas import (
    AuthRegisterRequest,
    AuthLoginResponse,
    AuthRegisterResponse,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthLoginResponse)
async def login_user(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDependency,
):
    """
    Login user and return access token.
    """

    return auth_service.get_authenticated(payload)


@router.post("/register", response_model=AuthRegisterResponse)
async def register_user(
    payload: AuthRegisterRequest,
    auth_service: AuthServiceDependency,
):
    """
    Register user and return message containing instructions for email verification.
    """

    return auth_service.create(payload)

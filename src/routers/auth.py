from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies import AuthServiceDependency
from src.schemas.auth import (
    AuthRegister,
    AuthLoginResponse,
    AuthRegisterResponse,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthLoginResponse)
async def login_user(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDependency,
):
    return auth_service.authenticate_user(payload)


@router.post("/register", response_model=AuthRegisterResponse)
async def register_user(
    payload: AuthRegister, auth_service: AuthServiceDependency
):
    return auth_service.create_user(payload)

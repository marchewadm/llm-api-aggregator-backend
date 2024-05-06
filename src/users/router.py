from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.auth import authenticate_user, create_access_token

from . import crud
from .schemas import UserCreate
from src.auth.schemas import Token
from .dependencies import db_dependency

from src.constants import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def create_user(
    user: UserCreate,
    db: db_dependency,
):
    return crud.create_user(db, user)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form_data.username, form_data.password, db)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )

    token = create_access_token(
        user.email,
        user.id,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": token, "token_type": "bearer"}

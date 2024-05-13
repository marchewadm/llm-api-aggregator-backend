from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import Token
from .auth import authenticate_user, create_access_token

from src.users.schemas import UserCreate
from src.users import crud

from src.database.dependencies import db_dependency
from src.constants import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/authentication", tags=["authentication"])


@router.post("/register")
async def create_user(db: db_dependency, user: UserCreate):
    response = crud.create_user(db, user)
    return response


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    """
    Login a user and return an access token.
    If user cannot be authenticated, e.g. because of wrong password, return a 401 status code.
    """

    user = authenticate_user(form_data.username, form_data.password, db)
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

from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from .schemas.response_schemas import CreateUserResponse, TokenResponse
from .auth import authenticate_user, create_access_token
from .openapi_responses import get_access_token_responses

from src.users.schemas.schemas import UserCreate
from src.users.crud import crud

from src.database.dependencies import db_dependency
from src.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from src.exceptions import NotAuthenticatedException


router = APIRouter(prefix="/authentication", tags=["authentication"])


@router.post("/register", response_model=CreateUserResponse)
async def create_user(db: db_dependency, user: UserCreate):
    """
    Inserts a new user into the database with a hashed password.

    Due to security reasons, the return value is always the same message, regardless of the outcome.

    If the email is already taken, the user with that email should be notified that someone tried
    to register with their email.

    User who tried to register should not be notified about the email being taken.
    """

    result = crud.create_user(db, user)
    return JSONResponse(content={"message": result.message})


@router.post(
    "/token",
    response_model=TokenResponse,
    responses={**get_access_token_responses},
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    """
    Login a user and return an access token.
    If user cannot be authenticated, e.g. because of wrong password or user does not exist, return a 401 status code.
    """

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise NotAuthenticatedException(
            message="Your email or password is incorrect. Please try again."
        )

    token = create_access_token(
        user.email,
        user.id,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return JSONResponse(content={"access_token": token, "token_type": "bearer"})

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from .crud import crud
from .schemas.schemas import UserUpdatePassword, UserUpdateProfile
from .schemas.response_schemas import (
    GetUserProfileResponse,
    UpdateUserPasswordResponse,
)
from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency

from src.exceptions import NotAuthenticatedException
from .openapi_responses import update_password_responses


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile", response_model=GetUserProfileResponse)
async def get_profile(auth: auth_dependency, db: db_dependency):
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return crud.get_desired_fields_by_user_id(
        db, auth["id"], ["name", "email", "avatar"]
    )


@router.patch(
    "/update-password",
    response_model=UpdateUserPasswordResponse,
    responses={**update_password_responses},
)
async def update_password(
    auth: auth_dependency, db: db_dependency, user_data: UserUpdatePassword
):
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )

    result = crud.update_user_password(db, auth["id"], user_data)
    if not result.success:
        raise NotAuthenticatedException(message=result.message)
    return JSONResponse(content={"message": result.message})


@router.patch("/update-profile")
async def update_profile(
    auth: auth_dependency, db: db_dependency, user_data: UserUpdateProfile
):
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return crud.update_user_profile(db, auth["id"], user_data)

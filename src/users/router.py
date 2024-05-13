from fastapi import APIRouter, HTTPException, status

from . import crud
from .schemas import UserUpdatePassword, UserUpdateProfile
from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/update-password")
async def update_password(
    auth: auth_dependency, db: db_dependency, user_data: UserUpdatePassword
):
    if auth is None:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return crud.update_user_password(db, auth["id"], user_data)


@router.post("/update-profile")
async def update_profile(
    auth: auth_dependency, db: db_dependency, user_data: UserUpdateProfile
):
    if auth is None:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return crud.update_user_profile(db, auth["id"], user_data)

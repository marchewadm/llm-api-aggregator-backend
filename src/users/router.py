from fastapi import APIRouter, HTTPException, status

from . import crud
from .schemas import UserCreate, UserUpdatePassword
from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def create_user(
    user: UserCreate,
    db: db_dependency,
):
    return crud.create_user(db, user)


@router.post("/update-password")
async def update_password(
    auth: auth_dependency,
    user_data: UserUpdatePassword,
    db: db_dependency,
):
    if auth is None:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return crud.update_user_password(db, user_data, auth["id"])

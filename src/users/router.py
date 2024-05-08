from fastapi import APIRouter

from . import crud
from .schemas import UserCreate
from src.database.dependencies import db_dependency


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def create_user(
    user: UserCreate,
    db: db_dependency,
):
    return crud.create_user(db, user)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.users import crud, schemas, dependencies


router = APIRouter(prefix="/users")


@router.get("/", tags=["users"])
async def read_users():
    return {"message": "Hello World User"}


@router.post("/register", tags=["users"])
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(dependencies.get_db),
):
    return crud.create_user(db, user)


@router.post("/login", tags=["users"])
async def login_user(
    user: schemas.UserLogin, db: Session = Depends(dependencies.get_db)
):
    return crud.login_user(db, user)

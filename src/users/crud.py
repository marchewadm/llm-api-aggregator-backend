from sqlalchemy.orm import Session

from src.users import models, schemas


def get_user(db: Session, user_id: int):
    return db.get(models.User, user_id)


def create_user(db: Session, user: schemas.UserCreate):
    return user

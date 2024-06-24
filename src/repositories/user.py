from typing import Optional

from sqlalchemy.orm import Session, load_only

from fastapi import Depends

from src.database.core import get_db

from src.user.models import User
from src.user.schemas import (
    UserBase,
    UserRegister,
    UserProfile,
    UserLogin,
)


class UserRepository:
    """
    Repository for user database related operations.
    """

    def __init__(self, db: Session = Depends(get_db)) -> None:
        # TODO: create base repository with db dependency
        self.db = db
        self.model = User

    def create(self, payload: UserRegister) -> None:
        self.db.add(
            User(
                name=payload.name,
                email=payload.email,
                password=payload.password,
            )
        )
        self.db.commit()
        return

    def get_profile_by_id(self, user_id: int) -> Optional[UserProfile]:
        user = (
            self.db.query(self.model)
            .options(
                load_only(
                    self.model.email,
                    self.model.name,
                    self.model.avatar,
                    self.model.passphrase,
                )
            )
            .filter(self.model.id == user_id)  # noqa
            .first()
        )
        if user:
            return UserProfile.model_validate(user)
        return

    def get_by_email(self, email: str) -> Optional[UserBase]:
        user = (
            self.db.query(self.model)
            .options(load_only(self.model.id))
            .filter(self.model.email == email)  # noqa
            .first()
        )
        if user:
            return UserBase.model_validate(user)
        return

    def get_authenticated_by_email(self, email: str) -> Optional[UserLogin]:
        user = (
            self.db.query(self.model)
            .options(load_only(self.model.id, self.model.password))
            .filter(self.model.email == email)  # noqa
            .first()
        )
        if user:
            return UserLogin.model_validate(user)
        return

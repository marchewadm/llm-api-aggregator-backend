from sqlalchemy.orm import Session, load_only

from fastapi import Depends

from src.database.core import get_db

from src.user.models import User
from src.user.schemas import UserRegister


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

    def get_by_id(self):
        pass

    def get_by_email(self, email: str) -> None | User:
        return (
            self.db.query(self.model)
            .options(load_only(self.model.id))
            .filter(self.model.email == email)  # noqa
            .first()
        )

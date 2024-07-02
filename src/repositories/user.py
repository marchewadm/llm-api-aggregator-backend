from sqlalchemy import update
from sqlalchemy.orm import Session

from fastapi import Depends

from src.database.core import get_db

from src.models.user import User

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for user database related operations.
    """

    def __init__(self, db: Session = Depends(get_db)) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db (Session): Database session.

        Returns:
            None
        """

        super().__init__(db, User)

    def update_password_by_id(
        self, user_id: int, hashed_new_password: str
    ) -> None:
        """
        Update the user's password by user id.

        Args:
            user_id (int): User id.
            hashed_new_password (str): Hashed new password.

        Returns:
            None
        """

        self.db.execute(
            update(self.model)
            .where(self.model.id == user_id)
            .values({self.model.password: hashed_new_password})
        )
        self.db.commit()

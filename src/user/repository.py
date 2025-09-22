from sqlalchemy import update
from sqlalchemy.orm import Session

from fastapi import Depends

from src.core.database import get_db

from src.shared.repository.base import BaseRepository

from .models import User


# TODO: Consider adding universal method for updating user's profile and password like "update_fields_by_id".
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

    def update_profile_by_id(self, user_id: int, payload: dict) -> None:
        """
        Update the user's profile by user id.

        Args:
            user_id (int): User id.
            payload (dict): The payload containing the optional fields to update such as name, email, avatar's URL.

        Returns:
            None
        """

        self.db.execute(
            update(self.model).where(self.model.id == user_id).values(payload)
        )
        self.db.commit()

    def update_passphrase_by_id(self, user_id: int, payload: dict) -> None:
        """
        Update the user's passphrase and salt by user id.

        Args:
            user_id (int): User id.
            payload (dict): The payload containing the salt and hashed passphrase.

        Returns:
            None
        """

        self.db.execute(
            update(self.model).where(self.model.id == user_id).values(payload)
        )
        self.db.commit()

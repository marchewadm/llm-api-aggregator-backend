from sqlalchemy import select, update
from sqlalchemy.orm import Session, load_only

from fastapi import Depends

from src.database.core import get_db

from src.models.user import User
from src.schemas.auth import AuthRegister


class UserRepository:
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

        TODO: create base repository with db dependency, create an argument to pass the model with type hinting.
        """

        self.db = db
        self.model = User

    def create(self, payload: AuthRegister) -> None:
        """
        Create a new user in the database.

        Args:
            payload (AuthRegister): User registration payload containing name, email and already hashed password.

        Returns:
            None
        """

        self.db.add(
            User(
                name=payload.name,
                email=payload.email,
                password=payload.password,
            )
        )
        self.db.commit()
        return

    def get_profile_by_id(self, user_id: int) -> User:
        """
        Get the user profile by user id.

        Args:
            user_id (int): User id.

        Returns:
            User: User object containing the user's email, name, avatar and passphrase.
        """

        return self.db.scalars(
            select(self.model)
            .options(
                load_only(
                    self.model.email,
                    self.model.name,
                    self.model.avatar,
                    self.model.passphrase,
                )
            )
            .where(self.model.id == user_id)
        ).first()

    def get_user_id_by_email(self, email: str) -> User:
        """
        Get the user by email.

        Args:
            email (str): User email.

        Returns:
            User: User object containing the user's id if found.
        """

        return self.db.scalars(
            select(self.model)
            .options(load_only(self.model.id, raiseload=True))
            .where(self.model.email == email)
        ).first()

    def get_user_id_and_password_by_email(self, email: str) -> User:
        """
        Get the user id and password by email.

        Args:
            email (str): User email.

        Returns:
            User: User object containing the user's id and password if found.
        """

        return self.db.scalars(
            select(self.model)
            .options(
                load_only(self.model.id, self.model.password, raiseload=True)
            )
            .where(self.model.email == email)
        ).first()

    def get_password_by_id(self, user_id: int) -> User:
        """
        Get the user password by user id.

        Args:
            user_id (int): User id.

        Returns:
            User: User object containing the user's password.
        """

        return self.db.scalars(
            select(self.model)
            .options(load_only(self.model.password, raiseload=True))
            .where(self.model.id == user_id)
        ).first()

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
        return

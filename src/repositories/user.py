from sqlalchemy import select
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

    def get_profile_by_id(self, user_id: int):
        """
        Get the user profile by user id.

        Args:
            user_id (int): User id.

        TODO: Add type hinting for the return value, maybe by using protocol.
        TODO: https://github.com/sqlalchemy/sqlalchemy/discussions/10760
        """

        return self.db.execute(
            select(
                self.model.email,
                self.model.name,
                self.model.avatar,
                self.model.passphrase,
            ).where(self.model.id == user_id)
        ).first()

    def get_by_email(self, email: str):
        """
        Get the user by email.

        Args:
            email (str): User email.

        TODO: Add type hinting for the return value, maybe by using protocol.
        TODO: https://github.com/sqlalchemy/sqlalchemy/discussions/10760
        """

        return (
            self.db.query(self.model)
            .options(load_only(self.model.id))
            .filter(self.model.email == email)  # noqa
            .first()
        )

    def get_id_and_password_by_email(self, email: str):
        """
        Get the user id and password by email.

        Args:
            email (str): User email.

        TODO: Add type hinting for the return value, maybe by using protocol.
        TODO: https://github.com/sqlalchemy/sqlalchemy/discussions/10760
        """

        return self.db.execute(
            select(self.model.id, self.model.password).where(
                self.model.email == email
            )
        ).first()

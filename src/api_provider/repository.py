from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, load_only

from fastapi import Depends

from src.core.database import get_db

from src.shared.repository.base import BaseRepository

from .models import ApiProvider


class ApiProviderRepository(BaseRepository[ApiProvider]):
    """
    Repository for api provider database related operations.
    """

    def __init__(self, db: Session = Depends(get_db)) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db (Session): Database session.

        Returns:
            None
        """

        super().__init__(db, ApiProvider)

    def get_all(self) -> Sequence[ApiProvider]:
        """
        Get all API providers.

        Returns:
            Sequence[ApiProvider]: A sequence of API provider objects containing the name of the provider.
        """

        return self.db.scalars(
            select(self.model).options(
                load_only(self.model.name, self.model.id)
            )
        ).all()

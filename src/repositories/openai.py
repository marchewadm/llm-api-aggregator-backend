from sqlalchemy.orm import Session

from fastapi import Depends

from src.core.database import get_db

from src.models.openai import OpenAiChatHistory

from .base import BaseRepository


class OpenAiRepository(BaseRepository[OpenAiChatHistory]):
    """
    Repository for OpenAI database related operations.
    """

    def __init__(self, db: Session = Depends(get_db)) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db (Session): Database session.

        Returns:
            None
        """

        super().__init__(db, OpenAiChatHistory)

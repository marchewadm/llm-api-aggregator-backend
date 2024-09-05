from uuid import UUID
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import Depends

from src.core.database import get_db

from src.shared.repository.base import BaseRepository

from .models import ChatHistory


class ChatHistoryRepository(BaseRepository[ChatHistory]):
    """
    Repository for chat history database related operations.
    """

    def __init__(self, db: Session = Depends(get_db)) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db (Session): Database session.

        Returns:
            None
        """

        super().__init__(db, ChatHistory)

    def get_chat_history_by_room_uuid(
        self, room_uuid: UUID
    ) -> Sequence[ChatHistory]:
        """
        Get the chat history based on the room's UUID.

        Args:
            room_uuid (UUID): The UUID of the room to get the chat history from.

        Returns:
            Sequence[ChatHistory]: A sequence of chat history objects.
        """

        return self.db.scalars(
            select(self.model).where(self.model.room_uuid == room_uuid)
        ).all()

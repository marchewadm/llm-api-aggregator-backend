import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from fastapi import Depends

from src.core.database import get_db

from src.shared.repository.base import BaseRepository

from .models import ChatRoom


class ChatRoomRepository(BaseRepository[ChatRoom]):
    """
    Repository for chat room database related operations.
    """

    def __init__(self, db: Session = Depends(get_db)) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db (Session): Database session.

        Returns:
            None
        """

        super().__init__(db, ChatRoom)

    def create(self, payload: dict) -> uuid.UUID:
        """
        Create a new record in the database. The method is overridden from the base repository to return the UUID of the
        chat room.

        Args:
            payload (dict): Payload containing the data to be created.

        Returns:
            uuid.UUID: The UUID of the chat room.
        """

        chat_room = self.model(**payload)

        self.db.add(chat_room)
        self.db.commit()

        return chat_room.room_uuid

    def get_all_by_user_id(self, user_id: int) -> Sequence[ChatRoom]:
        """
        Get all chat rooms by user ID.

        Args:
            user_id (int): The user's ID.

        Returns:
            Sequence[ChatRoom]: List of chat rooms.
        """

        return self.db.scalars(
            select(self.model)
            .options(joinedload(self.model.chat_history))
            .where(self.model.user_id == user_id)
        ).all()

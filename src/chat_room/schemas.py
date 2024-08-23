import uuid

from pydantic import BaseModel, PastDatetime, field_validator


class ChatRoom(BaseModel):
    room_uuid: uuid.UUID
    last_message: str
    last_message_sent_at: PastDatetime

    @field_validator("last_message")
    @classmethod
    def truncate_last_message(cls, value):
        """
        Shortens the last message if it exceeds the maximum allowed length, as it's only used as a title for the chat room.
        """

        max_chars_allowed = 200

        if len(value) > max_chars_allowed:
            return value[:max_chars_allowed]
        return value


class UserChatRoomsResponse(BaseModel):
    chat_rooms: list[ChatRoom]

    @field_validator("chat_rooms")
    @classmethod
    def sort_descending(cls, value: list[ChatRoom]):
        """
        Sort the chat rooms by 'last_message_sent_at' date in descending order.
        """

        if value:
            value.sort(key=lambda x: x.last_message_sent_at, reverse=True)
        return value

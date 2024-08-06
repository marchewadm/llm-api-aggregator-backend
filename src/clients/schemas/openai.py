from typing import Literal, Optional

from pydantic import BaseModel, PastDatetime


class OpenAiChatCompletionMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    created_at: PastDatetime


class OpenAiChatCompletionRequest(BaseModel):
    room_uuid: str
    ai_model: Literal[
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
    ]
    custom_instructions: Optional[str] = "You are a helpful assistant."
    messages: list[OpenAiChatCompletionMessage]

    def get_sorted_messages(self) -> list[dict]:
        """
        Get the messages sorted by created_at in ascending order.

        Returns:
            list[dict]: List of sorted messages containing the role and content.
        """

        sorted_messages = sorted(self.messages, key=lambda x: x.created_at)

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in sorted_messages
        ]


class OpenAiChatCompletionResponse(BaseModel):
    response_message: str
    created_at: PastDatetime

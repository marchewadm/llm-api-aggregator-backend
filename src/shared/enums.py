from enum import Enum


class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"


class AiModelEnum(str, Enum):
    gpt_4 = "gpt-4"
    gpt_4_turbo = "gpt-4-turbo"
    gpt_4o = "gpt-4o"
    gpt_4o_mini = "gpt-4o-mini"
    gpt_3_5_turbo = "gpt-3.5-turbo"

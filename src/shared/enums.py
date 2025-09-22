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
    gemini_1_5_flash = "gemini-1.5-flash"
    gemini_1_5_flash_8b = "gemini-1.5-flash-8b"
    gemini_1_5_pro = "gemini-1.5-pro"
    gemini_1_0_pro = "gemini-1.0-pro"

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Store the settings of the application by loading them from the environment variables.
    """

    DATABASE_URL: str
    ALLOWED_ORIGIN: str
    JWT_AUTH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_IN_MINUTES: int = 180

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file="./.env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Used to get the settings of the application.

    Returns:
        Settings: The settings of the application.
    """

    return Settings()


settings = get_settings()

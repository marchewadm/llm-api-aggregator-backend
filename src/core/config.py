from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Store the settings of the application by loading them from the environment variables.
    """

    DATABASE_URL: str
    REDIS_SERVER_HOST: str
    REDIS_SERVER_PORT: int
    ALLOWED_ORIGIN: str
    JWT_AUTH_SECRET_KEY: str
    FERNET_MASTER_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_IN_MINUTES: int = 180
    REDIS_API_KEYS_EXPIRE_IN_SEC: int = 900
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_S3_BUCKET_NAME: str
    AWS_S3_DOWNLOAD_PATH: str = str(Path("src/s3/tmp/"))

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file="./.env",
        env_file_encoding="utf-8",
        extra="allow",
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

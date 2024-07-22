from redis import Redis

from src.config import settings


def get_redis() -> Redis:
    """
    Get a Redis connection.

    Returns:
        Redis: A Redis connection object.
    """

    return Redis(
        host=settings.REDIS_SERVER_HOST, port=settings.REDIS_SERVER_PORT
    )

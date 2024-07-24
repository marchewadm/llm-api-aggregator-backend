import redis.asyncio as redis
from fastapi import Request


async def get_redis(request: Request) -> redis.Redis:
    """
    Get a Redis connection.

    Returns:
        Redis: The Redis connection.
    """

    return request.app.state.redis_client

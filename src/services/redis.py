from fastapi import Depends
from redis import asyncio as redis

from src.core.redis import get_redis
from src.schemas.api_key import ApiKeysResponse
from src.config import settings


class RedisService:
    """
    Service for Redis related operations.
    """

    def __init__(self, redis_client: redis.Redis = Depends(get_redis)) -> None:
        """
        Initializes the service with the Redis client.
        """

        self.redis_client = redis_client

    async def set_user_api_keys_in_cache(
        self, uuid: str, api_keys: ApiKeysResponse
    ):
        """
        Set the user's API keys in Redis. The API keys are stored in a set with the user's UUID as the key.

        Args:
            uuid (str): The user's UUID retrieved from user's JWT and stored in Redis.
            api_keys (ApiKeysResponse): The user's API keys retrieved from the database.

        Returns:
            None
        """

        if not api_keys.api_keys:
            return

        user_api_keys_list = f"user:{uuid}:api_keys"
        pipeline = self.redis_client.pipeline()

        current_api_keys = set(
            f"api_key:{api_key.id}" for api_key in api_keys.api_keys
        )

        if await self.redis_client.exists(user_api_keys_list):
            existing_api_keys = await self.redis_client.smembers(
                user_api_keys_list
            )
            api_keys_to_delete = existing_api_keys - current_api_keys

            for api_key_id in api_keys_to_delete:
                redis_key = f"user:{uuid}:{api_key_id}"

                await pipeline.delete(redis_key)
                await pipeline.srem(user_api_keys_list, api_key_id)

            api_keys_to_add = current_api_keys - existing_api_keys
        else:
            api_keys_to_add = current_api_keys

        for api_key in api_keys.api_keys:
            redis_key = f"user:{uuid}:api_key:{api_key.id}"

            api_key_data = {
                "key": api_key.key,
                "api_provider_id": str(api_key.api_provider_id),
                "api_provider_name": api_key.api_provider_name,
                "api_provider_lowercase_name": api_key.api_provider_lowercase_name,
            }

            await pipeline.hset(redis_key, mapping=api_key_data)
            await pipeline.expire(
                redis_key, settings.REDIS_API_KEYS_EXPIRE_IN_SEC
            )

            if f"api_key:{api_key.id}" in api_keys_to_add:
                await pipeline.sadd(user_api_keys_list, f"api_key:{api_key.id}")

        await pipeline.expire(
            user_api_keys_list, settings.REDIS_API_KEYS_EXPIRE_IN_SEC
        )
        await pipeline.execute()

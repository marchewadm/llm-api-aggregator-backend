from fastapi import Depends, HTTPException, status

from redis import asyncio as redis

from cryptography.fernet import Fernet

from src.core.redis import get_redis
from src.schemas.api_key import ApiKeysResponse
from src.config import settings
from src.utils.passphrase import passphrase_util


class RedisService:
    """
    Service for Redis related operations.
    """

    def __init__(self, redis_client: redis.Redis = Depends(get_redis)) -> None:
        """
        Initializes the service with the Redis client.
        """

        self.redis_client = redis_client

    async def get_user_specific_api_key(
        self, uuid: str, provider_name: str
    ) -> str:
        """
        Retrieve a specific API key for a user based on the API provider name.

        Args:
            uuid (str): The user's UUID retrieved from user's JWT and stored in Redis.
            provider_name (str): The name of the API provider (e.g., "openai").

        Raises:
            HTTPException: Raised with status code 401 if the user does not have any API keys stored in Redis.
            HTTPException: Raised with status code 404 if the user does not have an API key for the specified provider.

        Returns:
            str: The decrypted API key if found.
        """

        user_api_keys_list = f"user:{uuid}:api_keys"

        if not await self.redis_client.exists(user_api_keys_list):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide a passphrase to continue.",
            )

        api_key_ids = await self.redis_client.smembers(user_api_keys_list)

        for api_key_id in api_key_ids:
            redis_key = f"user:{uuid}:{api_key_id}"
            api_key_data = await self.redis_client.hgetall(redis_key)

            if api_key_data:
                if (
                    api_key_data.get("api_provider_lowercase_name", "").lower()
                    == provider_name.lower()
                ):
                    encrypted_key = api_key_data.get("key")

                    if not encrypted_key:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="API key not found.",
                        )

                    fernet_key = Fernet(settings.FERNET_MASTER_KEY)
                    decrypted_key = fernet_key.decrypt(
                        passphrase_util.convert_hex_to_bytes(encrypted_key)
                    )

                    return decrypted_key.decode()

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
            fernet_key = Fernet(settings.FERNET_MASTER_KEY)

            api_key_data = {
                "key": passphrase_util.convert_bytes_to_hex(
                    fernet_key.encrypt(api_key.key.encode())
                ),
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

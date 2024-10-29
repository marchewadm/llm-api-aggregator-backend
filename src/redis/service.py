from typing import TypedDict, Dict

from redis import asyncio as redis
from redis.commands.json.path import Path

from fastapi import Depends, Request, HTTPException, status

from cryptography.fernet import Fernet

from src.core.config import settings

from src.api_key.schemas import ApiKey, ApiKeysResponse

from src.shared.utils.passphrase import passphrase_util


async def get_redis(request: Request) -> redis.Redis:
    """
    Get a Redis connection.

    Returns:
        redis.Redis: The Redis connection.
    """

    return request.app.state.redis_client


class RedisApiKey(TypedDict):
    key: str
    api_provider_id: int
    api_provider_name: str


class RedisApiKeys(TypedDict):
    apiKeys: Dict[str, RedisApiKey]


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
        self, user_uuid: str, api_keys: ApiKeysResponse
    ) -> None:
        """
        Set the user's API keys in Redis.

        Args:
            user_uuid (str): The user's UUID.
            api_keys (ApiKeysResponse): The user's API keys.

        Returns:
            None
        """

        api_keys_list: list[ApiKey] = api_keys.api_keys

        if not api_keys_list:
            return await self.delete_user_api_keys_from_cache(user_uuid)

        user_data: RedisApiKeys = {"apiKeys": {}}
        redis_key = f"user:{user_uuid}"
        fernet_key = Fernet(settings.FERNET_MASTER_KEY)

        for api_key_obj in api_keys_list:
            user_data["apiKeys"][api_key_obj.api_provider_lowercase_name] = {
                "key": passphrase_util.convert_bytes_to_hex(
                    fernet_key.encrypt(api_key_obj.key.encode())
                ),
                "api_provider_id": api_key_obj.api_provider_id,
                "api_provider_name": api_key_obj.api_provider_name,
            }

        await self.redis_client.json().set(
            redis_key, Path.root_path(), user_data
        )
        await self.redis_client.expire(
            redis_key, settings.REDIS_API_KEYS_EXPIRE_IN_SEC
        )

    async def get_user_specific_api_key_from_cache(
        self, user_uuid: str, provider_name: str
    ) -> str:
        """
        Retrieve a specific API key for a user based on the API provider name.
        When the API key is found, extend the lifetime of all user keys in Redis to the expiry time constant set
        in the settings.

        Args:
            user_uuid (str): The user's UUID.
            provider_name (str): The name of the API provider (e.g. "openai").

        Raises:
            HTTPException: Raised with status code 403 if the user does not have any API keys stored in Redis.

        Returns:
            str: The decrypted API key if found.
        """

        redis_key = f"user:{user_uuid}"

        if not await self.is_redis_key_present(redis_key):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a passphrase to continue.",
            )

        api_keys: RedisApiKeys = await self.redis_client.json().get(redis_key)

        api_key_obj = api_keys["apiKeys"].get(provider_name.lower())

        if not api_key_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found.",
            )

        api_key = api_key_obj.get("key")

        await self.redis_client.expire(
            redis_key, settings.REDIS_API_KEYS_EXPIRE_IN_SEC
        )

        fernet_key = Fernet(settings.FERNET_MASTER_KEY)

        decrypted_api_key = fernet_key.decrypt(
            passphrase_util.convert_hex_to_bytes(api_key)
        ).decode()

        return decrypted_api_key

    async def delete_user_api_keys_from_cache(self, user_uuid: str) -> None:
        """
        Delete the user's API keys from Redis.

        Args:
            user_uuid (str): The user's UUID.

        Returns:
            None
        """

        redis_key = f"user:{user_uuid}"

        if not await self.is_redis_key_present(redis_key):
            return

        await self.redis_client.delete(redis_key)

    async def is_redis_key_present(self, redis_key: str) -> bool:
        """
        Checks if a given key exists in Redis.

        Args:
            redis_key (str): The Redis key to check for existence.

        Returns:
            bool: True if the key exists, False otherwise.
        """

        # Redis `exists` command returns 1 if the key exists or 0 if it does not.
        return await self.redis_client.exists(redis_key) == 1

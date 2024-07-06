from typing import Optional

from pydantic import BaseModel, SecretStr, field_validator


class ApiKey(BaseModel):
    key: str
    api_provider_id: Optional[int] = None
    api_provider_name: str
    api_provider_lowercase_name: str


class ApiKeysPassphrase(BaseModel):
    passphrase: SecretStr


class ApiKeyCreate(BaseModel):
    key: str
    api_provider_id: int


class ApiKeysUpdate(BaseModel):
    passphrase: SecretStr
    api_keys: Optional[list[ApiKeyCreate]] = None

    @field_validator("api_keys")
    @classmethod
    def validate_unique_api_provider_id(
        cls, api_keys: list[ApiKeyCreate]
    ) -> list[ApiKeyCreate]:
        unique_provider_ids: set[int] = set()

        for api_key in api_keys:
            if api_key.api_provider_id in unique_provider_ids:
                raise ValueError("API provider ID must be unique")
            unique_provider_ids.add(api_key.api_provider_id)

        return api_keys


class ApiKeysResponse(BaseModel):
    api_keys: Optional[list[ApiKey]] = None


class ApiKeysUpdateResponse(BaseModel):
    message: str

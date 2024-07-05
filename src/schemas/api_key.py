from typing import Optional

from pydantic import BaseModel, SecretStr


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


class ApiKeysResponse(BaseModel):
    api_keys: Optional[list[ApiKey]] = None


class ApiKeysUpdateResponse(BaseModel):
    message: str

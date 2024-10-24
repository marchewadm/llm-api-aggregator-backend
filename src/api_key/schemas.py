from typing import Optional, Annotated

from pydantic import BaseModel, SecretStr, field_validator, Field


class ApiKey(BaseModel):
    id: int
    key: str
    api_provider_id: Annotated[
        int | None, Field(serialization_alias="apiProviderId", default=None)
    ]
    api_provider_name: Annotated[
        str, Field(serialization_alias="apiProviderName")
    ]
    api_provider_lowercase_name: Annotated[
        str, Field(serialization_alias="apiProviderLowerCaseName")
    ]


class ApiKeysPassphraseRequest(BaseModel):
    passphrase: SecretStr


class ApiKeyCreate(BaseModel):
    key: str
    api_provider_id: Annotated[int, Field(validation_alias="apiProviderId")]


class ApiKeysUpdateRequest(BaseModel):
    passphrase: SecretStr
    api_keys: Annotated[
        list[ApiKeyCreate] | None,
        Field(validation_alias="apiKeys", default=None),
    ]

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
    api_keys: Annotated[
        list[ApiKey] | None, Field(serialization_alias="apiKeysDetails", default=None)
    ]


class ApiKeysUpdateResponse(BaseModel):
    message: str
    is_updated: bool

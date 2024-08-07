from typing import Annotated

from fastapi import Depends, Security

from src.services.auth import AuthService
from src.services.user import UserService
from src.services.api_provider import ApiProviderService
from src.services.api_key import ApiKeyService
from src.services.redis import RedisService
from src.services.openai import OpenAiService

from src.schemas.auth import AuthCurrentUser


AuthServiceDependency = Annotated[AuthService, Depends(AuthService)]
UserServiceDependency = Annotated[UserService, Depends(UserService)]
ApiProviderServiceDependency = Annotated[
    ApiProviderService, Depends(ApiProviderService)
]
ApiKeyServiceDependency = Annotated[ApiKeyService, Depends(ApiKeyService)]
RedisServiceDependency = Annotated[RedisService, Depends(RedisService)]
OpenAiServiceDependency = Annotated[OpenAiService, Depends(OpenAiService)]

AuthDependency = Annotated[
    AuthCurrentUser, Security(AuthService.get_current_user)
]

OpenAiApiKeyDependency = Annotated[str, Depends(OpenAiService.get_api_key)]

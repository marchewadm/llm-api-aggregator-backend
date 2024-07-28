from typing import Annotated

from fastapi import Depends

from .services.openai import OpenAiService

OpenAiServiceDependency = Annotated[OpenAiService, Depends(OpenAiService)]
OpenAiApiKeyDependency = Annotated[str, Depends(OpenAiService.get_api_key)]

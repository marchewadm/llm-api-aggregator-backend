from typing import Annotated

from fastapi import Depends, Security

from .service import GeminiService


GeminiServiceDependency = Annotated[GeminiService, Depends()]

GeminiApiKeyDependency = Annotated[str, Security(GeminiService.get_api_key)]

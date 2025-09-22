from typing import Annotated

from fastapi import Depends, Security

from .service import OpenAiService


OpenAiServiceDependency = Annotated[OpenAiService, Depends()]

OpenAiApiKeyDependency = Annotated[str, Security(OpenAiService.get_api_key)]

from typing import Annotated

from fastapi import Depends

from .services.openai import OpenAiService


OpenAiApiKeyDependency = Annotated[str, Depends(OpenAiService.get_api_key)]

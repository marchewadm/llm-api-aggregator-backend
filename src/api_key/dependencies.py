from typing import Annotated

from fastapi import Depends

from .service import ApiKeyService


ApiKeyServiceDependency = Annotated[ApiKeyService, Depends()]

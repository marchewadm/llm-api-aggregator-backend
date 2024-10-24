from typing import Annotated

from fastapi import Depends

from .service import ApiProviderService


ApiProviderServiceDependency = Annotated[ApiProviderService, Depends()]

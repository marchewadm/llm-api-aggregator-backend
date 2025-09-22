from typing import Annotated

from fastapi import Depends

from .service import RedisService


RedisServiceDependency = Annotated[RedisService, Depends()]

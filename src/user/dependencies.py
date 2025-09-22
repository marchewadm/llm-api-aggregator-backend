from typing import Annotated

from fastapi import Depends

from .service import UserService


UserServiceDependency = Annotated[UserService, Depends()]

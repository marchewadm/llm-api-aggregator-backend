from typing import Annotated

from fastapi import Depends

from src.auth.service import UserService

UserServiceDependency = Annotated[UserService, Depends(UserService)]

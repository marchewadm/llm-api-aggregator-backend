from typing import Annotated

from fastapi import Depends

from src.user.service import UserService

UserServiceDependency = Annotated[UserService, Depends(UserService)]

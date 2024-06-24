from typing import Annotated

from fastapi import Depends

from src.user.service import UserService
from src.user.schemas import UserCurrent
from src.user.utils import get_current_user


UserServiceDependency = Annotated[UserService, Depends(UserService)]

AuthDependency = Annotated[UserCurrent, Depends(get_current_user)]

from typing import Annotated

from fastapi import Depends

from src.services.auth import AuthService
from src.services.user import UserService

from src.schemas.auth import AuthCurrentUser

AuthServiceDependency = Annotated[AuthService, Depends(AuthService)]
UserServiceDependency = Annotated[UserService, Depends(UserService)]

AuthDependency = Annotated[
    AuthCurrentUser, Depends(AuthService.get_current_user)
]

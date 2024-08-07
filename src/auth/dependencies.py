from typing import Annotated

from fastapi import Depends, Security

from .service import AuthService
from .schemas import AuthCurrentUser


AuthServiceDependency = Annotated[AuthService, Depends()]

AuthDependency = Annotated[
    AuthCurrentUser, Security(AuthService.get_current_user)
]

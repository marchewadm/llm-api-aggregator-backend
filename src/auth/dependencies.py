from typing import Annotated
from fastapi import Depends
from .auth import get_current_user


auth_dependency = Annotated[dict, Depends(get_current_user)]

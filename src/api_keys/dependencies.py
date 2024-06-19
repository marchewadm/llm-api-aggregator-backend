from typing import Annotated
from fastapi import Depends
from .api_keys import get_user_fernet_key

api_dependency = Annotated[bytes, Depends(get_user_fernet_key)]

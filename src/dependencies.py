from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from .database.core import get_db


db_session_dependency = Annotated[Session, Depends(get_db)]

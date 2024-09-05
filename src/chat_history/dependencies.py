from typing import Annotated

from fastapi import Depends

from .service import ChatHistoryService


ChatHistoryServiceDependency = Annotated[ChatHistoryService, Depends()]

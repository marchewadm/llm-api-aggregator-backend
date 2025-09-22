from typing import Annotated

from fastapi import Depends

from .service import ChatRoomService


ChatRoomServiceDependency = Annotated[ChatRoomService, Depends()]

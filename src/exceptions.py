from fastapi import Request, status
from fastapi.responses import JSONResponse


class NotAuthenticatedException(Exception):
    def __init__(self, message: str):
        self.message = message


async def not_authenticated_exception_handler(
    request: Request, exc: NotAuthenticatedException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.message},
    )

from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppBaseException(Exception):
    def __init__(self, message: str):
        self.message = message


class NotAuthenticatedException(AppBaseException):
    pass


async def not_authenticated_exception_handler(
    request: Request, exc: NotAuthenticatedException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.message},
    )


class UserNotFoundException(AppBaseException):
    pass


async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )


class ConflictException(AppBaseException):
    pass


async def conflict_exception_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"message": exc.message}
    )

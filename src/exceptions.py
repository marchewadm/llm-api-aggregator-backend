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


class BadRequestException(AppBaseException):
    pass


async def bad_request_exception_handler(
    request: Request, exc: BadRequestException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message},
    )

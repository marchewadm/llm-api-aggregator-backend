from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .users.router import router as users_router
from .auth.router import router as auth_router
from .api_keys.router import router as api_keys_router
from .api_providers.router import router as api_providers_router

from .constants import ALLOWED_ORIGIN
from .exceptions import (
    NotAuthenticatedException,
    not_authenticated_exception_handler,
    UserNotFoundException,
    user_not_found_exception_handler,
    BadRequestException,
    bad_request_exception_handler,
)

exception_handlers = {
    NotAuthenticatedException: not_authenticated_exception_handler,
    UserNotFoundException: user_not_found_exception_handler,
    BadRequestException: bad_request_exception_handler,
}

app = FastAPI(exception_handlers=exception_handlers)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(api_keys_router)
app.include_router(api_providers_router)

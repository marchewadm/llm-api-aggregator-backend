from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .users.router import router as users_router
from .auth.router import router as auth_router
from .constants import ALLOWED_ORIGIN


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(auth_router)

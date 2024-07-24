from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from redis import asyncio as redis

from .api import api_router
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to manage the lifespan of the application.
    Connects to Redis on startup and closes the connection on shutdown.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None

    Returns:
        None
    """

    redis_client = redis.Redis(
        host=settings.REDIS_SERVER_HOST, port=settings.REDIS_SERVER_PORT, db=0
    )
    app.state.redis_client = redis_client
    yield
    await redis_client.flushdb()
    await redis_client.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

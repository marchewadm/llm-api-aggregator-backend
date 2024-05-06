from typing import Annotated
from fastapi import FastAPI, status, HTTPException, Depends

from .auth.auth import get_current_user

from .users import router as users_router

app = FastAPI()
app.include_router(users_router.router)

user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user_d: user_dependency):
    if user_d is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return {"user": user}

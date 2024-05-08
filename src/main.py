from typing import Annotated

from fastapi import FastAPI, status, HTTPException, Depends

from .users import router as users_router
from .auth.router import router as auth_router
from .auth.auth import get_current_user


app = FastAPI()
app.include_router(users_router.router)
app.include_router(auth_router)

user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user_d: user_dependency):
    if user_d is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return {"user": user}

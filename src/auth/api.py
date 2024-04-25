from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status

from auth.dependencies import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from auth.models import User
from settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    response: Response,
):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with username {username} and password {password} does not exist.",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    response.set_cookie(key="api_token", value=access_token, httponly=True, samesite="lax")
    return {"username": username}


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

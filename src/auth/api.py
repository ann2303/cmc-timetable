"""Module with auth handlers."""

from datetime import timedelta
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Query,
    Request,
    Response,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from auth.dependencies import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from auth.models import User
from settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")


@router.get("/login/", status_code=status.HTTP_200_OK)
async def login_page(request: Request):
    """Show log in page."""
    return templates.TemplateResponse(request=request, name="login.html")


@router.post("/login/")
async def login_for_access_token(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    response: Response,
    redirect_on_success: Annotated[str, Query()] = "/",
):
    """Log in user and redirect to required page."""
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with username {username} and password {password} does not exist.",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    response = RedirectResponse(url=redirect_on_success, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="api_token", value=access_token, httponly=True, samesite="lax")
    return response


@router.get("/logout/", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    """Log out user and redirect to root page."""
    response = RedirectResponse(url="/")
    response.delete_cookie(key="api_token", httponly=True, samesite="lax")
    return response


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Return user from request."""
    return current_user

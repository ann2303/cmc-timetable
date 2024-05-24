"""Service entrypoint module."""

import shutil
from contextlib import asynccontextmanager
from urllib import parse

import alembic.config
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse, RedirectResponse

from auth.api import router
from auth.dependencies import RequiresLoginError
from settings import settings
from timetable.api import router as timetable_router

import logging

from auth.dependencies import get_current_active_user
from auth.models import User
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
from fastapi.templating import Jinja2Templates


# run migrations to update database state
alembic_args = ["--raiseerr", "upgrade", "head"]
alembic.config.main(argv=alembic_args)

templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Activate lifespan context for the app."""

    # Create folder for additional information
    support_dir = settings.SUPPORT_DIR
    support_dir.mkdir(parents=True, exist_ok=True)

    yield

    # Clean up folder
    shutil.rmtree(support_dir.absolute())


app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
app.include_router(router)
app.include_router(timetable_router)


@app.exception_handler(RequiresLoginError)
async def redirect_to_login(request: Request, exc: RequiresLoginError):
    """Redirect to login page for pages, that require authentication."""
    return RedirectResponse(url=f"/auth/login/?redirect_on_success={parse.quote(request.url.path)}")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    """Check that server is up."""
    return {"status": "OK"}


@app.get("/", status_code=status.HTTP_200_OK)
async def index(request: Request, user: Annotated[User, Depends(get_current_active_user)]):
    """Show index page."""
    try:
        return templates.TemplateResponse(request=request, context={"admin": user.is_admin}, name="index.html")
    except Exception as e:
        logging.error(e)
    # return templates.TemplateResponse(request=request, context={"admin": user.is_admin}, name="index.html")

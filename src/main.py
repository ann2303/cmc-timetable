"""Service entrypoint module."""

import locale
import logging
import shutil
from contextlib import asynccontextmanager
from typing import Annotated
from urllib import parse

import alembic.config
from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from auth.api import router
from auth.dependencies import RequiresLoginError, get_current_active_user
from auth.models import User
from gettext_translate import _
from settings import settings
from timetable.api import router as timetable_router

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
    shutil.rmtree(support_dir.resolve())


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
    return templates.TemplateResponse(
        request=request, context={"admin": user.is_admin, "gettext": _}, name="index.html"
    )


languages = {"ru": ("ru_RU", "UTF-8"), "en": ("en_US", "UTF-8")}


@app.get("/choose_lang", status_code=status.HTTP_200_OK)
async def choose_lang(request: Request, user: Annotated[User, Depends(get_current_active_user)], lang: str):
    """Change locale for language."""

    try:
        locale.setlocale(locale.LC_ALL, languages[lang])
        return templates.TemplateResponse(
            request=request, context={"admin": user.is_admin, "gettext": _}, name="index.html"
        )
    except Exception as e:
        logging.error(e)

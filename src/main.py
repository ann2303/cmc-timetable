"""Service entrypoint module."""

from urllib import parse

import alembic.config
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse, RedirectResponse

from auth.api import router
from auth.dependencies import RequiresLoginError
from timetable.api import router as timetable_router

# run migrations to update database state
alembic_args = [
    "--raiseerr",
    "upgrade",
    "head",
]
alembic.config.main(argv=alembic_args)


app = FastAPI(default_response_class=ORJSONResponse)
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

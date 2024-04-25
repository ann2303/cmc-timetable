import alembic.config
from fastapi import FastAPI, status
from fastapi.responses import ORJSONResponse

from auth.api import router

# run migrations to update database state
alembic_args = [
    "--raiseerr",
    "upgrade",
    "head",
]
alembic.config.main(argv=alembic_args)


app = FastAPI(default_response_class=ORJSONResponse)
app.include_router(router)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    """Check that server is up."""
    return {"status": "OK"}

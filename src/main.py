import alembic.config
from fastapi import FastAPI, status

# run migrations to update database state
alembic_args = [
    "--raiseerr",
    "upgrade",
    "head",
]
alembic.config.main(argv=alembic_args)


app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    """Check that server is up."""
    return {"status": "OK"}

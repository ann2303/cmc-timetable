"""Module with api environment settings definition."""

from pathlib import Path

from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings

from gettext_translate import _


class Settings(BaseSettings):
    """Class for all server environment variables."""

    DB_HOST: str = Field("postgres", description=_("Database connection host name"))
    DB_PORT: PositiveInt = Field(5432, description=_("Database connection port"), ge=5000, le=6000)
    DB_NAME: str = Field(..., description=_("Name of the database to interact with"))
    DB_PASSWORD: str = Field(..., description=_("Password for database connection"))
    DB_USER: str = Field(..., description=_("User name to make database operations"))

    JWT_SECRET_KEY: str = Field(..., description=_("Secret key to generate JWT signature"))
    ALGORITHM: str = Field(..., description=_("Crypto algorithm to generate JWT signature"))
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = Field(
        ..., description=_("Time access tken is valid after creation"), le=60, ge=5
    )
    SUPPORT_DIR: Path = Field(
        Path(__file__) / "support_files",
        description=_("Path to the support directory where additional files with timetable will be saved"),
    )

    @property
    def database_dsn(self) -> str:
        """Return postgresql dsn with asynchronous driver asyncpg."""
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
            db=self.DB_NAME, user=self.DB_USER, password=self.DB_PASSWORD, host=self.DB_HOST, port=self.DB_PORT
        )

    @property
    def sync_database_dsn(self) -> str:
        """Return postgresql dsn with synchronous driver psycopg2."""
        return "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
            db=self.DB_NAME, user=self.DB_USER, password=self.DB_PASSWORD, host=self.DB_HOST, port=self.DB_PORT
        )


settings = Settings()

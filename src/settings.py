from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class for all server environment variables."""

    DB_HOST: str = Field("postgres", description="Database connection host name")
    DB_PORT: PositiveInt = Field(5432, description="Database connection port", ge=5000, le=6000)
    DB_NAME: str = Field(..., description="Name of the database to interact with")
    DB_PASSWORD: str = Field(..., description="Password for database connection")
    DB_USER: str = Field(..., description="User name to make database operations")

    JWT_SECRET_KEY: str = Field(..., description="Secret key to generate JWT signature")
    ALGORITHM: str = Field(..., description="Crypto algorithm to generate JWT signature")
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = Field(
        ..., description="Time access tken is valid after creation", le=60, ge=5
    )

    @property
    def database_dsn(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
            db=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
        )

    @property
    def sync_database_dsn(self) -> str:
        return "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
            db=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
        )


settings = Settings()

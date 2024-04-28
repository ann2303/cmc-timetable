"""Module with models for authentication purposes."""

from pydantic import BaseModel


class TokenData(BaseModel):
    """JWT payload model for token fields validation."""

    username: str | None = None


class User(BaseModel):
    """User model without sensitive data."""

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """User model equal to it's database representation."""

    hashed_password: str

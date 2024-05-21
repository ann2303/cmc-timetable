"""Module with models for authentication purposes."""

from typing import Any

from pydantic import BaseModel, EmailStr, field_validator

from gettext_translate import _


class TokenData(BaseModel):
    """JWT payload model for token fields validation."""

    username: str | None = None


class User(BaseModel):
    """User model without sensitive data."""

    username: str
    full_name: str
    email: EmailStr
    group: int | None
    is_admin: bool = False
    disabled: bool = False

    @field_validator("group")
    @classmethod
    def check_group(cls, value: Any):
        """Check that group value is in right range."""
        if value is None:
            return value
        if not (101 <= value <= 630):
            raise ValueError(_("{} parameter must be between 101 and 630").format("group"))
        return value

    class Config:
        """Define configuration to get values from class attributes."""

        from_attributes = True


class UserInDB(User):
    """User model equal to it's database representation."""

    hashed_password: str

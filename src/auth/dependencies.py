"""Module with auth handlers dependencies."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

from auth.models import TokenData, User, UserInDB
from db.dao import AsyncSession
from db.user.dao import UserDAO
from settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RequiresLoginError(Exception):
    """Exception on invalid authentication."""

    pass


def _verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str) -> UserInDB | None:
    """Get user by username and password."""
    async with AsyncSession.begin() as session:
        user = await UserDAO.get_user_by_username(username=username, session=session)
    if not user:
        return None
    if not _verify_password(password, user.hashed_password):
        return None
    return UserInDB.model_validate(user)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create JWT for authentication."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(api_token: Annotated[str | None, Cookie()] = None):
    """Get current user based on cookie."""
    credentials_exception = RequiresLoginError()
    if api_token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(api_token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    async with AsyncSession.begin() as session:
        user = await UserDAO.get_user_by_username(username=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return User.model_validate(user)


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Return current active user."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

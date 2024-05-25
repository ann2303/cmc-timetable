"""Module with python representation of user in database."""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class UserORM(Base):
    """User table mapper."""

    __tablename__ = "users"
    username: Mapped[str] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    group: Mapped[int | None] = mapped_column(sa.SmallInteger, index=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    disabled: Mapped[bool] = mapped_column(default=False)

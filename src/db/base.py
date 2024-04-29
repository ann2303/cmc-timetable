"""Module with base class for all ORM entity classes."""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.schema import MetaData


class Base(DeclarativeBase):
    """Base class for all server tables."""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            # this comes from sqlalchemy's default naming convention, so, postgres also used that
            "uq": "%(table_name)s_%(column_0_name)s_key",  # as in postgres by default
            "ck": "%(table_name)s_%(column_0_name)s_check",  # as in postgres by default
            "fk": "%(table_name)s_%(column_0_name)s_fkey",  # as in postgres by default
            "pk": "%(table_name)s_pkey",  # as in postgres by default
        }
    )

"""Module with base database operations, entity agnostic."""

from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSessionClass
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import settings

async_engine = create_async_engine(settings.database_dsn, echo=False, pool_size=10, pool_recycle=3600)
AsyncSession = async_sessionmaker(bind=async_engine, expire_on_commit=False)


T = TypeVar("T")


class DAO:
    """Database access object.

    Only base table operations like CRUD, common for different entities.
    """

    @staticmethod
    async def select_row(object_type: T, session: AsyncSessionClass, select_cols: dict) -> T | None:
        """Select one row in a table."""
        filters = [getattr(object_type, key) == value for key, value in select_cols.items()]
        stmt = select(object_type).where(*filters)
        return await session.scalar(stmt)

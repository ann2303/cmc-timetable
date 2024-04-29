"""Module with database operations with users."""

from db.dao import DAO, AsyncSessionClass
from db.user.user import UserORM


class UserDAO:
    """Database access object for User entity."""

    @staticmethod
    async def get_user_by_username(session: AsyncSessionClass, username: str) -> UserORM | None:
        """Get user by username."""
        return await DAO.select_row(UserORM, session=session, select_cols={"username": username})

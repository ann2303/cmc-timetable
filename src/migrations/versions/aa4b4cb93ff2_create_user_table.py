"""create user table.

Revision ID: aa4b4cb93ff2
Revises: 
Create Date: 2024-04-29 20:36:33.600053

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aa4b4cb93ff2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade to new migration."""
    users = op.create_table(
        "users",
        sa.Column("username", sa.String, primary_key=True),
        sa.Column("full_name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("group", sa.SmallInteger, nullable=True, index=True),
        sa.Column("is_admin", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("disabled", sa.Boolean, nullable=False, server_default=sa.false()),
    )
    op.bulk_insert(
        users,
        [
            {
                "username": "admin",
                "full_name": "Ezhov Andrei Vladimirovich",
                "email": "ezhovandr@gmail.com",
                "hashed_password": "$2b$12$OBWCsDBRVBeOXDYX2iUSreXDRxaWESMKwrDlPIasgQSXmNBfZwb6.",
                "is_admin": True,
                "group": 527,
            },
            {
                "username": "Ann_Ili",
                "full_name": "Ilina Anna Aleksandrovna",
                "email": "annili@yandex.ru",
                "hashed_password": "$2b$12$fS2R6iFl0rVttAweqQXbSekOUomy/eMgPlEquLGnqR2j0e6Y8dAEC",
                "is_admin": False,
                "group": 527,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade to previous migration."""
    op.drop_table("users")

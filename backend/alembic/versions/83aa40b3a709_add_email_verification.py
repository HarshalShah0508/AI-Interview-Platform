"""add email verification

Revision ID: 83aa40b3a709
Revises: 3921f137e4ca
Create Date: 2026-08-08 18:13:07.621131
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "83aa40b3a709"
down_revision: Union[str, Sequence[str], None] = "3921f137e4ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "email_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    # Remove the temporary server default.
    # Existing users remain verified (TRUE),
    # while new users will use the SQLAlchemy model default.
    op.alter_column(
        "users",
        "email_verified",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "users",
        "email_verified",
    )
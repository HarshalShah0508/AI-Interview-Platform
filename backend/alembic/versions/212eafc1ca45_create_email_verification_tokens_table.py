"""create email verification tokens table

Revision ID: 212eafc1ca45
Revises: 83aa40b3a709
Create Date: 2026-08-09 10:54:11.346952
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "212eafc1ca45"
down_revision: Union[str, Sequence[str], None] = "83aa40b3a709"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "email_verification_tokens",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "token",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "expires_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        op.f("ix_email_verification_tokens_id"),
        "email_verification_tokens",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_email_verification_tokens_token"),
        "email_verification_tokens",
        ["token"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_email_verification_tokens_token"),
        table_name="email_verification_tokens",
    )

    op.drop_index(
        op.f("ix_email_verification_tokens_id"),
        table_name="email_verification_tokens",
    )

    op.drop_table(
        "email_verification_tokens",
    )
"""add content column to post table

Revision ID: 03c79582e5be
Revises: 8b46763b69d7
Create Date: 2022-06-26 04:32:33.925301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03c79582e5be'
down_revision = '8b46763b69d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass

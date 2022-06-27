"""add published, created_At column to posts table

Revision ID: c27979c976ad
Revises: 8522e18933ce
Create Date: 2022-06-26 04:57:41.045850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c27979c976ad'
down_revision = '8522e18933ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.String(), nullable=False, server_default='TRUE'))

    op.add_column('posts',sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),)

    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass

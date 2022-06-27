"""create foreign key

Revision ID: 8522e18933ce
Revises: 423f2f6d20df
Create Date: 2022-06-26 04:51:19.873647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8522e18933ce'
down_revision = '423f2f6d20df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass

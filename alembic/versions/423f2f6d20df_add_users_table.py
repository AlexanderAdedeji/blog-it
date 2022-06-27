"""add users table

Revision ID: 423f2f6d20df
Revises: 03c79582e5be
Create Date: 2022-06-26 04:39:10.911308

"""
from http import server
from sqlite3 import Timestamp
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '423f2f6d20df'
down_revision = '03c79582e5be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
         sa.Column( "id",sa.Integer(), primary_key=True, nullable=False),
         sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(),nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('email')
        
        )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass

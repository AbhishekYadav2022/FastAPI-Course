"""Add Content Column To Posts Table

Revision ID: ab9da673cae3
Revises: d07a84761a55
Create Date: 2022-12-21 15:46:09.306460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab9da673cae3'
down_revision = 'd07a84761a55'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')

"""Add Last Few Columns To Posts Column

Revision ID: 00a0bbc4ee37
Revises: 2b69966c8308
Create Date: 2022-12-21 16:21:50.952962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00a0bbc4ee37'
down_revision = '2b69966c8308'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

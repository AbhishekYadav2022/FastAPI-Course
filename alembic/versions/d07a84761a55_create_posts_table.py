"""Create Posts Table

Revision ID: d07a84761a55
Revises: 
Create Date: 2022-12-20 18:31:54.444046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd07a84761a55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))

def downgrade() -> None:
    op.drop_table('posts')

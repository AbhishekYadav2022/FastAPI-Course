"""Add foreign-key To Posts Table

Revision ID: 2b69966c8308
Revises: 667636d88b7e
Create Date: 2022-12-21 16:06:20.577635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b69966c8308'
down_revision = '667636d88b7e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
"""Add Users Table

Revision ID: 667636d88b7e
Revises: ab9da673cae3
Create Date: 2022-12-21 15:54:40.172224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '667636d88b7e'
down_revision = 'ab9da673cae3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('users')

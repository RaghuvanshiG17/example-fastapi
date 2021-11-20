"""add few columns to posts table

Revision ID: 350f9a2c7104
Revises: 7d5fbd31cd06
Create Date: 2021-11-20 21:56:33.155212

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = '350f9a2c7104'
down_revision = '7d5fbd31cd06'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass

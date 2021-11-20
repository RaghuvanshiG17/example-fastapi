"""added contet column to table

Revision ID: 28701f4e00ca
Revises: 29bf62de16af
Create Date: 2021-11-20 20:12:48.523393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28701f4e00ca'
down_revision = '29bf62de16af'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass

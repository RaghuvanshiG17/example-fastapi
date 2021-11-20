"""add phone number

Revision ID: 6798e38d5424
Revises: 86d3b982319c
Create Date: 2021-11-20 22:09:24.471767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6798e38d5424'
down_revision = '86d3b982319c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
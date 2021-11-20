"""added users table

Revision ID: 1958790855cd
Revises: 28701f4e00ca
Create Date: 2021-11-20 21:09:01.574072

"""
from re import M
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = '1958790855cd'
down_revision = '28701f4e00ca'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email',sa.String(), nullable=False),
        sa.Column('password',sa.String(), nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone = True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )
    pass


def downgrade():
    op.drop_table('users')
    pass

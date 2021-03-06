"""empty message

Revision ID: 5f26ea74ee51
Revises: 6263ea80a86c
Create Date: 2020-11-17 23:02:51.568698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f26ea74ee51'
down_revision = '6263ea80a86c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('credits', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'credits')
    # ### end Alembic commands ###

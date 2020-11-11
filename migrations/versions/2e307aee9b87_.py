"""empty message

Revision ID: 2e307aee9b87
Revises: 4cc1ea620934
Create Date: 2020-11-09 01:12:29.039924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e307aee9b87'
down_revision = '4cc1ea620934'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('caption', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'caption')
    # ### end Alembic commands ###

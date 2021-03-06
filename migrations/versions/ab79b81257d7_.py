"""empty message

Revision ID: ab79b81257d7
Revises: b86d1670ecbb
Create Date: 2020-11-23 01:02:46.906683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab79b81257d7'
down_revision = 'b86d1670ecbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('image_url', sa.Text(), nullable=True))
    op.add_column('post', sa.Column('user_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'user_id')
    op.drop_column('post', 'image_url')
    # ### end Alembic commands ###

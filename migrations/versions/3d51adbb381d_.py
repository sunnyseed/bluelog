"""empty message

Revision ID: 3d51adbb381d
Revises: babdd3ec9106
Create Date: 2020-06-02 08:55:10.099129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d51adbb381d'
down_revision = 'babdd3ec9106'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('pic_url', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'pic_url')
    # ### end Alembic commands ###

"""empty message

Revision ID: 29846fab2d43
Revises: 52e129d00b28
Create Date: 2024-05-12 16:21:08.407153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29846fab2d43'
down_revision = '52e129d00b28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_active', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_column('last_active')

    # ### end Alembic commands ###

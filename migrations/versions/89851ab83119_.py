"""empty message

Revision ID: 89851ab83119
Revises: 1a48e3596bd7
Create Date: 2024-05-15 09:06:30.801412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89851ab83119'
down_revision = '1a48e3596bd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('color', sa.String(length=20), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('frequency', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    # ### end Alembic commands ###

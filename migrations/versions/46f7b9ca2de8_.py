"""empty message

Revision ID: 46f7b9ca2de8
Revises: 4b31795ed4d1
Create Date: 2019-07-21 23:43:33.245079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46f7b9ca2de8'
down_revision = '4b31795ed4d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('ticket_type', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookings', 'ticket_type')
    # ### end Alembic commands ###

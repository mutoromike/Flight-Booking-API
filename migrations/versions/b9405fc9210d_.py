"""empty message

Revision ID: b9405fc9210d
Revises: bb6d41fee339
Create Date: 2019-07-18 14:42:29.843095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9405fc9210d'
down_revision = 'bb6d41fee339'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flights', 'is_admin')
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')
    op.add_column('flights', sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
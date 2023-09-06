"""empty message

Revision ID: 04e0e666d724
Revises: e7149effbb1f
Create Date: 2023-09-06 21:13:54.270538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04e0e666d724'
down_revision = 'e7149effbb1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###

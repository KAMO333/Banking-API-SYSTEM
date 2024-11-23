"""Create account table

Revision ID: 8507e8c3561e
Revises: da672b2d131d
Create Date: 2024-11-16 16:25:46.117149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8507e8c3561e'
down_revision = 'da672b2d131d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.VARCHAR(length=13),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.VARCHAR(length=13),
               nullable=False)

    # ### end Alembic commands ###

"""Added user_id column to Account model

Revision ID: da672b2d131d
Revises: 78deb6036eed
Create Date: 2024-11-16 14:34:06.270224
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'da672b2d131d'
down_revision = '78deb6036eed'
branch_labels = None
depends_on = None

def upgrade():
    # Get the current table's columns
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [column['name'] for column in inspector.get_columns('account')]

    # Add 'user_id' column only if it does not exist
    if 'user_id' not in columns:
        with op.batch_alter_table('account', schema=None) as batch_op:
            batch_op.add_column(sa.Column('user_id', sa.String(length=13), nullable=True))

    # Create unique constraint on 'user_id' column
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_user_id', ['user_id'])

def downgrade():
    # Drop unique constraint on 'user_id' column
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_id', type_='unique')

    # Drop 'user_id' column from 'account' table
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_column('user_id')

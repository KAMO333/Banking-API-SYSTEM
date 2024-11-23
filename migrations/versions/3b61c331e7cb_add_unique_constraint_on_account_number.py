"""Add unique constraint on account_number

Revision ID: 3b61c331e7cb
Revises: 8507e8c3561e
Create Date: 2024-11-17 19:37:19.057955
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '3b61c331e7cb'
down_revision = '8507e8c3561e'
branch_labels = None
depends_on = None


def upgrade():
    # Check if the 'account_number' column already exists in the 'account' table
    inspector = inspect(op.get_bind())
    columns = [column['name'] for column in inspector.get_columns('account')]

    if 'account_number' not in columns:
        # Step 1: Add the 'account_number' column as nullable
        with op.batch_alter_table('account', schema=None) as batch_op:
            batch_op.add_column(
                sa.Column('account_number', sa.String(length=12), nullable=True)
            )

        # Step 2: Populate default unique values for existing rows
        op.execute("""
        UPDATE account
        SET account_number = id || '_ACC'
        WHERE account_number IS NULL
        """)

        # Step 3: Make the column non-nullable
        with op.batch_alter_table('account', schema=None) as batch_op:
            batch_op.alter_column('account_number', nullable=False)

        # Step 4: Add the unique constraint
        with op.batch_alter_table('account', schema=None) as batch_op:
            batch_op.create_unique_constraint('uq_account_number', ['account_number'])


def downgrade():
    # Step 1: Drop the unique constraint
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_constraint('uq_account_number', type_='unique')

    # Step 2: Drop the 'account_number' column
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_column('account_number')

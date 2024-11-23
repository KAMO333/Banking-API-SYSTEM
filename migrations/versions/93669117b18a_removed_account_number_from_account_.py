"""Removed account_number from Account model

Revision ID: 93669117b18a
Revises: 8a320ea6edd3
Create Date: 2024-11-17 21:30:08.842069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93669117b18a'
down_revision = '8a320ea6edd3'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('account', 'account_number')

def downgrade():
    pass

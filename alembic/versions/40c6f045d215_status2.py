"""status2

Revision ID: 40c6f045d215
Revises: e99df689bd1e
Create Date: 2025-12-09 15:20:14.707205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40c6f045d215'
down_revision: Union[str, Sequence[str], None] = 'e99df689bd1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('invoices_rls', sa.Column('status2', sa.String(), nullable=False, server_default='second status'))

def downgrade():
    op.drop_column('invoices_rls', 'status2')
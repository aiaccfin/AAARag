"""status2

Revision ID: 8abce7f23580
Revises: 634a30a04e4e
Create Date: 2025-12-09 15:00:21.639626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8abce7f23580'
down_revision: Union[str, Sequence[str], None] = '634a30a04e4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('payments_rls', sa.Column('status2', sa.String(), nullable=False, server_default='second status'))

def downgrade():
    op.drop_column('payments_rls', 'status2')
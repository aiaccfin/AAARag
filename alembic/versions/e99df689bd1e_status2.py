"""status2

Revision ID: e99df689bd1e
Revises: 8abce7f23580
Create Date: 2025-12-09 15:05:16.896864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e99df689bd1e'
down_revision: Union[str, Sequence[str], None] = '8abce7f23580'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('payments_rls', sa.Column('status2', sa.String(), nullable=False, server_default='second status'))

def downgrade():
    op.drop_column('payments_rls', 'status2')
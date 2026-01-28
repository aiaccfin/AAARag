"""remove payer, notes-json

Revision ID: 634a30a04e4e
Revises: 0b2073098e2f
Create Date: 2025-12-04 10:27:50.784064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '634a30a04e4e'
down_revision: Union[str, Sequence[str], None] = '0b2073098e2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""remove payer, notes-json

Revision ID: 0b2073098e2f
Revises: 0d450e3ffdc6
Create Date: 2025-12-04 10:25:03.138035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b2073098e2f'
down_revision: Union[str, Sequence[str], None] = '0d450e3ffdc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

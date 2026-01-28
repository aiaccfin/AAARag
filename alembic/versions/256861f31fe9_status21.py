"""status21

Revision ID: 256861f31fe9
Revises: 0bbfba581f72
Create Date: 2025-12-09 15:36:04.173064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '256861f31fe9'
down_revision: Union[str, Sequence[str], None] = '0bbfba581f72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

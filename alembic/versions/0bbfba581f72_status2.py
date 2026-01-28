"""status2

Revision ID: 0bbfba581f72
Revises: 5443d73f2b57
Create Date: 2025-12-09 15:35:31.021288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bbfba581f72'
down_revision: Union[str, Sequence[str], None] = '5443d73f2b57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

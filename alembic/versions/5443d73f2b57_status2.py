"""status2

Revision ID: 5443d73f2b57
Revises: 40c6f045d215
Create Date: 2025-12-09 15:32:34.646893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5443d73f2b57'
down_revision: Union[str, Sequence[str], None] = '40c6f045d215'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

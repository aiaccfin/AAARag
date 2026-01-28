"""update invoice embedding

Revision ID: 6bba0cc0b9ed
Revises: b08b440bf349
Create Date: 2025-12-24 17:55:59.682590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bba0cc0b9ed'
down_revision: Union[str, Sequence[str], None] = 'b08b440bf349'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

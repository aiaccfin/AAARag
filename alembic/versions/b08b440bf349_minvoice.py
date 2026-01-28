"""minvoice

Revision ID: b08b440bf349
Revises: 256861f31fe9
Create Date: 2025-12-12 16:44:51.175883

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b08b440bf349'
down_revision: Union[str, Sequence[str], None] = '256861f31fe9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

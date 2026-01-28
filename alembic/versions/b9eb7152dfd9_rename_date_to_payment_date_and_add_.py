"""rename date to payment_date and add defaults

Revision ID: b9eb7152dfd9
Revises: d48533e2bc00
Create Date: 2025-12-03 15:14:01.328448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9eb7152dfd9'
down_revision: Union[str, Sequence[str], None] = 'd48533e2bc00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""rename date to payment_date and add defaults

Revision ID: 0d450e3ffdc6
Revises: b9eb7152dfd9
Create Date: 2025-12-03 15:17:17.696869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d450e3ffdc6'
down_revision: Union[str, Sequence[str], None] = 'b9eb7152dfd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""update invoice embedding

Revision ID: 824c5ae32c5f
Revises: 6bba0cc0b9ed
Create Date: 2025-12-24 17:57:31.119533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '824c5ae32c5f'
down_revision: Union[str, Sequence[str], None] = '6bba0cc0b9ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

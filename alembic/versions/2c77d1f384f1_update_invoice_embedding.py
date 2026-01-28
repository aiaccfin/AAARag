"""update invoice embedding

Revision ID: 2c77d1f384f1
Revises: 824c5ae32c5f
Create Date: 2025-12-24 17:58:06.494955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c77d1f384f1'
down_revision: Union[str, Sequence[str], None] = '824c5ae32c5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""new audits logic

Revision ID: 623c1b66f99c
Revises: 120e674c5f8e
Create Date: 2026-05-12 00:43:18.509219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '623c1b66f99c'
down_revision: Union[str, Sequence[str], None] = '120e674c5f8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

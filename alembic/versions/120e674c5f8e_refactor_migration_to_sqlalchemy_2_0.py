"""refactor: migration to SQLAlchemy 2.0

Revision ID: 120e674c5f8e
Revises: 4bf57a10b3c4
Create Date: 2026-05-12 00:12:21.039996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '120e674c5f8e'
down_revision: Union[str, Sequence[str], None] = '4bf57a10b3c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

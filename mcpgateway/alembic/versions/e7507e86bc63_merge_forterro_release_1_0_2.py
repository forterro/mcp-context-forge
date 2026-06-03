"""merge_forterro_release_1_0_2

Revision ID: e7507e86bc63
Revises: 8b22c624dd73, a5b1cec45457, b3c4d5e6f7a8, e28566875fa4
Create Date: 2026-06-03 15:47:15.900656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7507e86bc63'
down_revision: Union[str, Sequence[str], None] = ('8b22c624dd73', 'a5b1cec45457', 'b3c4d5e6f7a8', 'e28566875fa4')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

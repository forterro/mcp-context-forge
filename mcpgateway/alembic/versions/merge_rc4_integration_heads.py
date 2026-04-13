"""Merge RC4 integration migration heads.

Revision ID: rc4_merge_integration
Revises: b3c4d5e6f7a8, f7a2b1c3d4e5
Create Date: 2026-04-13
"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "rc4_merge_integration"
down_revision: Union[str, Sequence[str], None] = ("b3c4d5e6f7a8", "f7a2b1c3d4e5")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Merge heads — no schema changes."""
    pass


def downgrade() -> None:
    """Reverse merge — no schema changes."""
    pass

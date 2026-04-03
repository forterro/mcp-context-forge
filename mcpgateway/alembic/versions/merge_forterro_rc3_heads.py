"""Merge Forterro RC3 heads.

Merges the three topic-branch migrations into a single head so that
Alembic does not refuse to run ``upgrade head``.

Revision ID: forterro_rc3_merge
Revises: a1b2c3d4e5f6, b3c4d5e6f7a8, f7a2b1c3d4e5
Create Date: 2026-04-03

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "forterro_rc3_merge"
down_revision: Union[str, Sequence[str], None] = (
    "a1b2c3d4e5f6",
    "b3c4d5e6f7a8",
    "f7a2b1c3d4e5",
)
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Merge-only migration — nothing to do."""


def downgrade() -> None:
    """Merge-only migration — nothing to do."""

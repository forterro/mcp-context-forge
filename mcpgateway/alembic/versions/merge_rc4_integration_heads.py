"""Merge RC4 integration migration heads.

Merges all four parallel heads from the clean integration rebuild:
- b3c4d5e6f7a8 (gateway tool filters)
- f7a2b1c3d4e5 (team OIDC sync)
- a1b2c3d4e5f6 (user gateway credentials — personal credential store)
- c2d3e4f5a6b7 (manage plugins team admin — meta-tools)

Revision ID: rc4_merge_integration
Revises: b3c4d5e6f7a8, f7a2b1c3d4e5, a1b2c3d4e5f6, c2d3e4f5a6b7
Create Date: 2026-04-13
"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "rc4_merge_integration"
down_revision: Union[str, Sequence[str], None] = ("b3c4d5e6f7a8", "f7a2b1c3d4e5", "a1b2c3d4e5f6", "c2d3e4f5a6b7")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Merge heads — no schema changes."""
    pass


def downgrade() -> None:
    """Reverse merge — no schema changes."""
    pass

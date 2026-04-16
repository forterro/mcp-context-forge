# -*- coding: utf-8 -*-
"""Merge all Forterro RC4 integration heads

Revision ID: f0r7err0_rc4
Revises: 5126ced48fd0, 376a0d2c500f, a1b2c3d4e5f6, a8f3b2c1d4e5, b3c4d5e6f7a8, d3e4f5a6b7c8, k5e6f7g8h9i0, q1b2c3d4e5f6
Create Date: 2026-07-10 12:00:00.000000
"""

# Standard
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "f0r7err0_rc4"
down_revision: Union[str, Sequence[str], None] = (
    "5126ced48fd0",
    "376a0d2c500f",
    "a1b2c3d4e5f6",
    "a8f3b2c1d4e5",
    "b3c4d5e6f7a8",
    "d3e4f5a6b7c8",
    "k5e6f7g8h9i0",
    "q1b2c3d4e5f6",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""

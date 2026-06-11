# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""merge forterro release 1.0.2 heads

Revision ID: ed013636438d
Revises: 0a089912b5f0, 8b22c624dd73, a5b1cec45457, b3c4d5e6f7a8
Create Date: 2026-06-11 16:53:42.740100

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "ed013636438d"
down_revision: Union[str, Sequence[str], None] = ("0a089912b5f0", "8b22c624dd73", "a5b1cec45457", "b3c4d5e6f7a8")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema (no-op merge)."""


def downgrade() -> None:
    """Downgrade schema (no-op merge)."""

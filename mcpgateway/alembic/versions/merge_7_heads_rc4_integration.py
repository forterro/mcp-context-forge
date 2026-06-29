# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Merge seven divergent Alembic heads for RC4 integration.

Revision ID: 664ce26d3339
Revises: 5126ced48fd0, 8b22c624dd73, a8f3b2c1d4e5, aa1b2c3d4e5f, b3c4d5e6f7a8, k5e6f7g8h9i0, q1b2c3d4e5f6
Create Date: 2026-04-28

This no-op merge reconciles the seven divergent heads that existed during the
RC4 integration. It was originally shipped in image ``1.0.0-RC4-forterro-72``
and the production database is stamped on this revision. The file was later
dropped when the forterro release/1.0.2 merge chain was regenerated, which left
production databases orphaned (``Can't locate revision identified by
'664ce26d3339'``). It is restored here, and the current head
``ed013636438d`` descends from it, so a database stamped on ``664ce26d3339``
upgrades cleanly to a single head.
"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "664ce26d3339"
down_revision: Union[str, Sequence[str], None] = (
    "5126ced48fd0",
    "8b22c624dd73",
    "a8f3b2c1d4e5",
    "aa1b2c3d4e5f",
    "b3c4d5e6f7a8",
    "k5e6f7g8h9i0",
    "q1b2c3d4e5f6",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema (no-op merge)."""


def downgrade() -> None:
    """Downgrade schema (no-op merge)."""

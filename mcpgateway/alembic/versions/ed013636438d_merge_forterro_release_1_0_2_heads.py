# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""merge forterro release 1.0.2 heads

Revision ID: ed013636438d
Revises: e7507e86bc63, 0a089912b5f0
Create Date: 2026-06-11 16:53:42.740100

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "ed013636438d"
# Descend from the previous (-06-03) no-op merge ``e7507e86bc63`` and the new
# upstream head ``0a089912b5f0`` (add_numeric_id_to_email_users). This keeps the
# old merge revision reachable so databases stamped on ``e7507e86bc63`` upgrade
# cleanly, while the three forterro feature heads remain consumed by
# ``e7507e86bc63``. A fresh database still resolves to a single head here.
down_revision: Union[str, Sequence[str], None] = ("e7507e86bc63", "0a089912b5f0")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema (no-op merge)."""


def downgrade() -> None:
    """Downgrade schema (no-op merge)."""

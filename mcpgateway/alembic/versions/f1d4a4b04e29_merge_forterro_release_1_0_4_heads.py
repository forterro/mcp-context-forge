# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""merge forterro release 1.0.4 heads

Revision ID: f1d4a4b04e29
Revises: 6c0e5f8a9b1d, a5b1cec45457, 664ce26d3339
Create Date: 2026-06-29 12:00:00.000000

No-op merge unifying the divergent heads produced by rebuilding the forterro
patch set on upstream v1.0.4:

- ``6c0e5f8a9b1d`` upstream v1.0.4 head (add_gateway_lifecycle_fields)
- ``a5b1cec45457`` feat/team-management (rename_oidc_group_id_to_oidc_group_ids)
- ``664ce26d3339`` RC4 7-head integration merge, which already consumes the
  personal-credential-store head (``8b22c624dd73``) and the gateway tool
  filters head (``b3c4d5e6f7a8``). Descending from it keeps PROD databases
  stamped on ``664ce26d3339`` (image ``1.0.0-RC4-forterro-72``) upgradable to a
  single head instead of orphaning.

Regenerate this file whenever the integration branch is rebuilt on a new
upstream release.
"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "f1d4a4b04e29"
down_revision: Union[str, Sequence[str], None] = (
    "6c0e5f8a9b1d",
    "a5b1cec45457",
    "664ce26d3339",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema (no-op merge)."""


def downgrade() -> None:
    """Downgrade schema (no-op merge)."""

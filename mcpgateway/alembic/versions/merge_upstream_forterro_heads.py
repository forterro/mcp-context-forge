# -*- coding: utf-8 -*-
"""Merge upstream and forterro migration heads

Revision ID: a1b2c3d4e5f6
Revises: a7f3c9e1b2d4, f7a2b1c3d4e5
Create Date: 2026-03-30 12:00:00.000000

Merge the upstream head (225bde88217e - add_grant_source_to_team_members)
with the Forterro head (f7a2b1c3d4e5 - add_oidc_sync_to_teams) into a
single revision so that `alembic upgrade head` succeeds.
"""

# Standard
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = ("225bde88217e", "f7a2b1c3d4e5")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Merge heads — no schema changes needed."""
    pass


def downgrade() -> None:
    """Merge heads — no schema changes needed."""
    pass

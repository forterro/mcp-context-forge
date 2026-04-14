# -*- coding: utf-8 -*-
"""Merge Forterro RC4 feature heads

Revision ID: m1a2b3c4d5e6
Revises: a1b2c3d4e5f6, b3c4d5e6f7a8, d3e4f5a6b7c8, f7a2b1c3d4e5
Create Date: 2026-04-14 18:00:00.000000

Merge all 4 alembic heads into a single head for the RC4 integration:
- a1b2c3d4e5f6: add_user_gateway_credentials_table (personal-credential-store)
- b3c4d5e6f7a8: add_gateway_tool_filters (gateway-tool-filters)
- d3e4f5a6b7c8: add_binding_reference_id (upstream RC-3)
- f7a2b1c3d4e5: add_oidc_sync_to_teams (team-management)
"""

# Standard
from typing import Sequence, Union

# Third-Party
# from alembic import op
# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "m1a2b3c4d5e6"
down_revision: Union[str, Sequence[str], None] = (
    "a1b2c3d4e5f6",
    "b3c4d5e6f7a8",
    "d3e4f5a6b7c8",
    "f7a2b1c3d4e5",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Merge migration — no schema changes."""
    pass


def downgrade() -> None:
    """Merge migration — no schema changes."""
    pass

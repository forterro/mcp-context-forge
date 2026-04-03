"""Add tools_include and tools_exclude columns to gateways table.

Revision ID: b3c4d5e6f7a8
Revises: a7f3c9e1b2d4
Create Date: 2026-04-03 10:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b3c4d5e6f7a8"
down_revision = "a7f3c9e1b2d4"
branch_labels = None
depends_on = None


def upgrade():
    """Add tool filter columns to gateways."""
    with op.batch_alter_table("gateways", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("tools_include", sa.JSON(), nullable=True, comment="Glob patterns to include tools (whitelist)")
        )
        batch_op.add_column(
            sa.Column("tools_exclude", sa.JSON(), nullable=True, comment="Glob patterns to exclude tools (blacklist)")
        )


def downgrade():
    """Remove tool filter columns from gateways."""
    with op.batch_alter_table("gateways", schema=None) as batch_op:
        batch_op.drop_column("tools_exclude")
        batch_op.drop_column("tools_include")

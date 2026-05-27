"""Merge all heads into single head for 1.0.2-forterro integration

Revision ID: f1020001merge
Revises: 5126ced48fd0, 8b22c624dd73, a8f3b2c1d4e5, aa1b2c3d4e5f, b3c4d5e6f7a8, k5e6f7g8h9i0, q1b2c3d4e5f6, a5b1cec45457, e28566875fa4
Create Date: 2026-05-27
"""

from alembic import op  # noqa: F401

# revision identifiers, used by Alembic.
revision = "f1020001merge"
down_revision = (
    "5126ced48fd0",
    "8b22c624dd73",
    "a8f3b2c1d4e5",
    "aa1b2c3d4e5f",
    "b3c4d5e6f7a8",
    "k5e6f7g8h9i0",
    "q1b2c3d4e5f6",
    "a5b1cec45457",
    "e28566875fa4",
)
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

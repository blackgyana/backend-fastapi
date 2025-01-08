"""add TIMESTAMP created_at in bookings

Revision ID: ddf69fd43d9a
Revises: 57a9685c255f
Create Date: 2025-01-08 13:28:45.666333

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ddf69fd43d9a"
down_revision: Union[str, None] = "57a9685c255f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "bookings",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("bookings", "created_at")
    # ### end Alembic commands ###

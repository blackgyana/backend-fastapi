"""Add ON DELETE CASCADE to rooms.hotel_id

Revision ID: cdf5358d0588
Revises: bb9aca825325
Create Date: 2025-11-09 15:07:39.307667

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cdf5358d0588"
down_revision: Union[str, None] = "bb9aca825325"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('rooms_hotel_id_fkey', 'rooms', type_='foreignkey')
    op.create_foreign_key(
        'rooms_hotel_id_fkey', 'rooms', 'hotels',
        ['hotel_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('rooms_hotel_id_fkey', 'rooms', type_='foreignkey')
    op.create_foreign_key(
        'rooms_hotel_id_fkey', 'rooms', 'hotels',
        ['hotel_id'], ['id']
    )

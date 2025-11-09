"""add cascade delete for rooms_facilities.room_id

Revision ID: 39b4965d1410
Revises: cdf5358d0588
Create Date: 2025-11-09 15:11:21.072508

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "39b4965d1410"
down_revision: Union[str, None] = "cdf5358d0588"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('rooms_facilities_room_id_fkey', 'rooms_facilities', type_='foreignkey')
    op.create_foreign_key(
        'rooms_facilities_room_id_fkey', 'rooms_facilities', 'rooms',
        ['room_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('rooms_facilities_room_id_fkey', 'rooms_facilities', type_='foreignkey')
    op.create_foreign_key(
        'rooms_facilities_room_id_fkey', 'rooms_facilities', 'rooms',
        ['room_id'], ['id']
    )

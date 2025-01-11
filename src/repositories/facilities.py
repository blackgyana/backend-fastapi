from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomsFacilities, RoomsFacilitiesAdd
from src.repositories.base import BaseRepository
from src.repositories.base import BaseRepository
from sqlalchemy import select, insert, delete


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacilities

    async def set(self, room_id: int, facilities_ids: list[int]):
        room_facilities = (
            select(RoomsFacilitiesOrm.facility_id)
            .filter_by(room_id=room_id)
            .subquery(name='room_facilities')
        )
        facilities_ids_add = (
            select(FacilitiesOrm.id)
            .filter(FacilitiesOrm.id.not_in(select(room_facilities)),
                    FacilitiesOrm.id.in_(facilities_ids))
            .subquery(name='facilities_to_add')
        )
        facilities_ids_del = (
            select(FacilitiesOrm.id)
            .filter(FacilitiesOrm.id.in_(select(room_facilities)),
                    FacilitiesOrm.id.not_in(facilities_ids))
            .subquery(name='facilities_to_add')
        ) if facilities_ids else room_facilities
        insert_stmt = (
            insert(RoomsFacilitiesOrm)
            .from_select(['room_id', 'facility_id'],
                        select(room_id, facilities_ids_add))
        )
        await self.session.execute(insert_stmt)
        delete_stmt = (
            delete(RoomsFacilitiesOrm)
            .filter(RoomsFacilitiesOrm.facility_id.in_(select(facilities_ids_del)))
            .filter_by(room_id=room_id)
        )
        await self.session.execute(delete_stmt)

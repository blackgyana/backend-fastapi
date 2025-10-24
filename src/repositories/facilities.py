from sqlalchemy.exc import IntegrityError, NoResultFound
from asyncpg import ForeignKeyViolationError, UniqueViolationError
from src.exceptions import ObjectAlreadyExistsException, ObjectInBulkNotFoundException, UnknownException
from src.repositories.mappers.mappers import FacilitiesDataMapper, RoomsFacilitiesDataMapper
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from sqlalchemy import select, insert, delete


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomsFacilitiesDataMapper

    async def set(self, room_id: int, facilities_ids: list[int]):
        room_facilities = (
            select(RoomsFacilitiesORM.facility_id)
            .filter_by(room_id=room_id)
            .subquery(name="room_facilities")
        )
        facilities_ids_add = (
            select(FacilitiesORM.id)
            .filter(
                FacilitiesORM.id.not_in(select(room_facilities)),
                FacilitiesORM.id.in_(facilities_ids),
            )
            .subquery(name="facilities_to_add")
        )
        facilities_ids_del = (
            (
                select(FacilitiesORM.id)
                .filter(
                    FacilitiesORM.id.in_(select(room_facilities)),
                    FacilitiesORM.id.not_in(facilities_ids),
                )
                .subquery(name="facilities_to_add")
            )
            if facilities_ids
            else room_facilities
        )
        insert_stmt = insert(RoomsFacilitiesORM).from_select(
            ["room_id", "facility_id"], select(room_id, facilities_ids_add)
        )
        try:
            await self.session.execute(insert_stmt)
            delete_stmt = (
                delete(RoomsFacilitiesORM)
                .filter(RoomsFacilitiesORM.facility_id.in_(select(facilities_ids_del)))
                .filter_by(room_id=room_id)
            )
            await self.session.execute(delete_stmt)
        except UniqueViolationError:
            raise ObjectAlreadyExistsException
        except (ForeignKeyViolationError, NoResultFound, IntegrityError):
            raise ObjectInBulkNotFoundException
        except:
            raise UnknownException

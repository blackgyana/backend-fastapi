

from datetime import date
import logging
from src.exceptions.repositories import ObjectInBulkNotFoundException
from src.models.facilities import FacilitiesORM
from src.schemas.facilities import RoomsFacilitiesAdd
from src.schemas.rooms import RoomAddDTO, RoomAddRequest, RoomDTO, RoomPatch, RoomPatchRequest
from src.services.base import BaseService


class RoomsService(BaseService):

    async def get_rooms(self, hotel_id: int, date_from: date, date_to: date):
        self.check_dates(date_from, date_to)
        return await self.db.rooms.get_filtered_by_dates(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    
    async def get_room(self, hotel_id:int, room_id:int):
        return await self.db.rooms.get_one(hotel_id=hotel_id, room_id=room_id)

    async def add_room(self, hotel_id: int, room_data: RoomAddRequest):
        _room_data = RoomAddDTO(hotel_id=hotel_id, **room_data.model_dump())
        room: RoomDTO = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomsFacilitiesAdd(room_id=room.id, facility_id=fid) for fid in set(room_data.facilities_ids)
        ]
        if rooms_facilities_data:
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room

    async def update_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        _room_data = RoomAddDTO(**room_data.model_dump(), hotel_id=hotel_id)
        room = await self.db.rooms.update(_room_data, id=room_id, hotel_id=hotel_id)
        facilities = await self.db.facilities.get_filtered(FacilitiesORM.id.in_(room_data.facilities_ids))
        if len(facilities) < len(room_data.facilities_ids):
            raise ObjectInBulkNotFoundException
        await self.db.rooms_facilities.set(room_id=room_id, facilities_ids=room_data.facilities_ids)
        await self.db.commit()
        return room
    
    async def update_room_part(self, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
        clear_data = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(**clear_data, hotel_id=hotel_id)
        room = await self.db.rooms.update(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in clear_data:
            facilities = await self.db.facilities.get_filtered(FacilitiesORM.id.in_(clear_data['facilities_ids']))
            if len(facilities) < len(clear_data['facilities_ids']):
                raise ObjectInBulkNotFoundException
            await self.db.rooms_facilities.set(room_id=room_id, facilities_ids=clear_data['facilities_ids'])
        await self.db.commit()
        return room
    
    async def delete_room(self, hotel_id: int, room_id: int):
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()


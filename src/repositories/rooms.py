from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from src.repositories.mappers.mappers import RoomsDataMapper
from src.repositories.utils import filtered_free_rooms_ids
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomDTO, RoomWithRels
from src.repositories.base import BaseRepository

class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomsDataMapper

    async def get_filtered_by_dates(self, hotel_id: int, date_from: date, date_to: date):
        
        filtered_rooms_ids = filtered_free_rooms_ids(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(filtered_rooms_ids))
        )
        result = await self.session.execute(query)
        return [self.mapper.to_domain_entity(model) for model in result.scalars().all()]

    async def get_one(self, hotel_id: int, room_id: int):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(hotel_id=hotel_id, id=room_id)
        )
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        return self.mapper.to_domain_entity(res) if res else None



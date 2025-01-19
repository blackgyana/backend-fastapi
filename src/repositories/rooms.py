from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from src.repositories.utils import filtered_free_rooms_ids
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room, RoomWithRels
from src.repositories.base import BaseRepository

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_dates(self, hotel_id: int, date_from: date, date_to: date):
        
        filtered_rooms_ids = filtered_free_rooms_ids(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(filtered_rooms_ids))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model) for model in result.scalars().all()]

        



from datetime import date
from sqlalchemy import select
from src.models.rooms import RoomsOrm
from src.repositories.utils import filtered_free_rooms_ids
from src.schemas.hotels import Hotel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_dates(
            self,
            date_from: date,
            date_to: date,
            limit: int,
            offset: int,
            title: str | None = None,
            location: str | None = None
        ):

        filtered_rooms_ids = filtered_free_rooms_ids(
            date_from=date_from, date_to=date_to)

        filtered_rooms_hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(filtered_rooms_ids))
        )
        query = select(HotelsOrm).filter(
            HotelsOrm.id.in_(filtered_rooms_hotels_ids))
        if title:
            query = query.filter(
                HotelsOrm.title.icontains(title.strip()),
            )
        if location:
            query = query.filter(
                HotelsOrm.location.icontains(location.strip()),
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [Hotel.model_validate(model) for model in result.scalars().all()]

from datetime import date
from sqlalchemy import select
from src.repositories.mappers.mappers import HotelsDataMapper
from src.models.rooms import RoomsORM
from src.repositories.utils import filtered_free_rooms_ids
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelsDataMapper

    async def get_filtered_by_dates(
        self,
        date_from: date,
        date_to: date,
        limit: int,
        offset: int,
        title: str | None = None,
        location: str | None = None,
    ):
        filtered_rooms_ids = filtered_free_rooms_ids(date_from=date_from, date_to=date_to)

        filtered_rooms_hotels_ids = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(filtered_rooms_ids))
        )
        query = select(HotelsORM).filter(HotelsORM.id.in_(filtered_rooms_hotels_ids))
        if title:
            query = query.filter(
                HotelsORM.title.icontains(title.strip()),
            )
        if location:
            query = query.filter(
                HotelsORM.location.icontains(location.strip()),
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.mapper.to_domain_entity(model) for model in result.scalars().all()]

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.exceptions.repositories import ObjectNotFoundException
from src.repositories.mappers.mappers import RoomsDataMapper, RoomsWithRelsDataMapper
from src.repositories.utils import filtered_free_rooms_ids
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from sqlalchemy.exc import NoResultFound


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomsDataMapper

    async def get_filtered_by_dates(self, hotel_id: int, date_from: date, date_to: date):
        filtered_rooms_ids = filtered_free_rooms_ids(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(filtered_rooms_ids))
        )
        result = await self.session.execute(query)
        return [RoomsWithRelsDataMapper.to_domain_entity(model) for model in result.scalars().all()]

    async def get_one(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        try:
            res = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return RoomsWithRelsDataMapper.to_domain_entity(res) if res else None

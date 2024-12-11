from sqlalchemy import insert, select
from schemas.hotels import Hotel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self,
                      title: str,
                      location: str,
                      limit: int,
                      offset: int
                      ) -> list[Hotel]:
        query = select(self.model)
        if title:
            query = query.filter(
                self.model.title.icontains(title.strip()),
            )
        if location:
            query = query.filter(
                self.model.location.icontains(location.strip()),
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def add(self, hotel: Hotel) -> Hotel:
        new_hotel = HotelsOrm(**hotel.model_dump())
        self.session.add(new_hotel)
        await self.session.flush()
        return new_hotel
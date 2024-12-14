from sqlalchemy import insert, select
from schemas.hotels import Hotel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

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
        return [Hotel.model_validate(model) for model in result.scalars().all()]

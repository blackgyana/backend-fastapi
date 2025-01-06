from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self,
                      title: str,
                      description: str,
                      limit: int,
                      offset: int
                      ) -> list[Room]:
        query = select(self.model)
        if title:
            query = query.filter(
                self.model.title.icontains(title.strip()),
            )
        if description:
            query = query.filter(
                self.model.location.icontains(description.strip()),
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [Room.model_validate(model) for model in result.scalars().all()]


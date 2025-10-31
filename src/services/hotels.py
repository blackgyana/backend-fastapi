

from datetime import date
from src.api.dependencies import PaginationDep
from src.services.base import BaseService


class HotelsService(BaseService):

    async def get_hotels(self,
                         pagination: PaginationDep,
                         date_from: date,
                         date_to: date,
                         title: str | None,
                         location: str | None):
    
        limit = pagination.per_page
        offset = pagination.per_page * (pagination.page - 1)

        if date_from >= date_to:
            raise HTTPException(
                status_code=400, detail='Дата въезда не может быть позже даты выезда')

        return await db.hotels.get_filtered_by_dates(
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
            title=title,
            location=location,
        )

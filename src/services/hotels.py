

from datetime import date
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelAddDTO, HotelUpdateDTO
from src.services.base import BaseService


class HotelsService(BaseService):

    async def get_hotels(self,
                         pagination: PaginationDep,
                         date_from: date,
                         date_to: date,
                         title: str | None,
                         location: str | None
                         ):

        limit = pagination.per_page
        offset = pagination.per_page * (pagination.page - 1)

        self.check_dates(date_from, date_to)

        return await self.db.hotels.get_filtered_by_dates(
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
            title=title,
            location=location,
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get(id=hotel_id)

    async def add_hotel(self, hotel_data: HotelAddDTO):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel
    
    async def update_hotel(self, hotel_id: int, hotel_data: HotelAddDTO):
        hotel = await self.db.hotels.update(hotel_data, id=hotel_id)
        await self.db.commit()
        return hotel
    
    async def update_hotel_part(self, hotel_id: int, hotel_data: HotelUpdateDTO):
        hotel = await self.db.hotels.update(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()
        return hotel
    
    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

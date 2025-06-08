from datetime import timedelta
from fastapi import HTTPException
from src.repositories.mappers.mappers import BookingsDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.repositories.utils import filtered_free_rooms_ids
from src.schemas.bookings import BookingAddDTO


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingsDataMapper

    async def add_booking(self, data: BookingAddDTO, hotel_id: int):
        "Добавляем бронирование если номер в списке свободных"
        if data.date_to - data.date_from <= timedelta(0):
            raise HTTPException(status_code=400, detail="Invalid dates period.")
        free_rooms_ids = await self.session.execute(
            filtered_free_rooms_ids(
                date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
            )
        )
        if data.room_id in free_rooms_ids.scalars().all():
            return await self.add(data)
        raise HTTPException(status_code=400, detail="No such free rooms left.")

from datetime import date, timedelta
from fastapi import HTTPException
from sqlalchemy import select
from src.exceptions.services import FreeRoomsNotFoundException, InvalidDatesException
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
            raise InvalidDatesException
        free_rooms_ids = await self.session.execute(
            filtered_free_rooms_ids(
                date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
            )
        )
        if data.room_id in free_rooms_ids.scalars().all():
            return await self.add(data)
        raise FreeRoomsNotFoundException

    async def get_bookings_with_today_checkin(self):
        "Получить бронирования с заселением сегодня"
        query = (
            select(BookingsORM)
            .filter(BookingsORM.date_from == date.today())
            )
        result = await self.session.execute(query)

        return [self.mapper.to_domain_entity(obj) for obj in result.scalars().all()]
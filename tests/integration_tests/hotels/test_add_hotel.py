
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelAddDTO


async def test_add_hotel():
    hotel_data = HotelAddDTO(title='Тестовый отель', location='Сочи')
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add(hotel_data)
        await db.commit()
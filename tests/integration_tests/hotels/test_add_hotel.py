from src.utils.db_manager import DBManager
from src.schemas.hotels import HotelAddDTO


async def test_add_hotel(db: DBManager):
    hotel_data = HotelAddDTO(title="Тестовый отель", location="Сочи")
    await db.hotels.add(hotel_data)
    await db.commit()

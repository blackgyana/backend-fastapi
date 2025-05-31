
from datetime import date
from src.utils.db_manager import DBManager
from src.schemas.bookings import BookingAddDTO, BookingUpdateDTO


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAddDTO(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2024, month=5, day=20),
        date_to=date(year=2024, month=5, day=25),
        price=6000      
    )
    new_booking = await db.bookings.add(booking_data)
    assert new_booking
    booking = await db.bookings.get(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id

    booking_update = BookingUpdateDTO(price=4000)
    booking = await db.bookings.update(booking_update, exclude_unset=True, id=new_booking.id)
    assert booking.price == 4000

    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert not booking
    await db.commit()

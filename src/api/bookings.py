from fastapi import APIRouter
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAdd, BookingsAddRequest, Bookings
from src.schemas.rooms import Room

router = APIRouter(prefix='/bookings')


@router.get('', summary='Получить все бронирования')
async def get_bookings(uid: UserIdDep, db: DBDep) -> list[Bookings]:
    return await db.bookings.get_all(user_id=uid)


@router.post('', summary='Добавить бронирование')
async def add_bookings(uid: UserIdDep, db: DBDep, booking_data: BookingsAddRequest):
    room: Room = await db.rooms.get(id=booking_data.room_id)
    _booking_data = BookingsAdd(
        **booking_data.model_dump(), user_id=uid, price=room.price)
    new_booking: Bookings = await db.bookings.add(_booking_data)
    await db.commit()
    return {'status': 'OK', 'booking': new_booking}


@router.delete('/{booking_id}', summary='Удалить бронирование')
async def get_bookings(uid: UserIdDep, db: DBDep, booking_id: int):
    await db.bookings.delete(id=booking_id, user_id=uid)
    await db.commit()
    return {'status': 'OK'}

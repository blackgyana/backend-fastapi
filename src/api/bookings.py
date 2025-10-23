from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import FreeRoomsNotFoundException, ObjectNotFoundException
from src.schemas.bookings import BookingAddDTO, BookingAddRequest, BookingDTO
from src.schemas.rooms import RoomDTO

router = APIRouter(prefix="/bookings")


@router.get("/", summary="Получить все бронирования")
@cache(expire=30)
async def get_bookings(db: DBDep) -> list[BookingDTO]:
    return await db.bookings.get_filtered()


@router.get("/me", summary="Получить все мои бронирования")
@cache(expire=30)
async def get_my_bookings(uid: UserIdDep, db: DBDep) -> list[BookingDTO]:
    return await db.bookings.get_filtered(user_id=uid)


@router.post("", summary="Добавить бронирование")
async def add_booking(uid: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    try:
        room: RoomDTO = await db.rooms.get(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail='Номер не найден')
    _booking_data = BookingAddDTO(**booking_data.model_dump(), user_id=uid, price=room.price)
    try:
        booking: BookingDTO = await db.bookings.add_booking(
            _booking_data, hotel_id=booking_data.hotel_id
        )
        await db.commit()
    except FreeRoomsNotFoundException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    return {"status": "OK", "data": booking}


@router.delete("/{booking_id}", summary="Удалить бронирование")
async def delete_booking(uid: UserIdDep, db: DBDep, booking_id: int):
    await db.bookings.delete(id=booking_id, user_id=uid)
    await db.commit()
    return {"status": "OK"}

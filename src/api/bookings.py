from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions.base import UnknownException
from src.exceptions.framework import BookingNotFoundHTTPException, FreeRoomsNotFoundHTTPException, RoomNotFoundHTTPException, UnknownHTTPException
from src.exceptions.repositories import ObjectNotFoundException
from src.exceptions.services import FreeRoomsNotFoundException
from src.schemas.bookings import BookingAddDTO, BookingAddRequest, BookingDTO
from src.schemas.hotels import HotelDTO
from src.schemas.rooms import RoomDTO
from src.services.bookings import BookingsService

router = APIRouter(prefix="/bookings")


@router.get("/", summary="Получить все бронирования")
@cache(expire=30)
async def get_bookings(db: DBDep) -> list[BookingDTO]:
    return await BookingsService(db).get_bookings()


@router.get("/me", summary="Получить все мои бронирования")
@cache(expire=30)
async def get_my_bookings(uid: UserIdDep, db: DBDep) -> list[BookingDTO]:
    return await BookingsService(db).get_my_bookings(uid)


@router.post("", summary="Добавить бронирование")
async def add_booking(uid: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    try:
        booking = await BookingsService(db).add_booking(uid, booking_data)
    except ObjectNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except ObjectNotFoundException:
        raise BookingNotFoundHTTPException from ex
    except FreeRoomsNotFoundException as ex:
        raise FreeRoomsNotFoundHTTPException from ex
    return {"status": "OK", "data": booking}


@router.delete("/{booking_id}", summary="Удалить бронирование")
async def delete_booking(uid: UserIdDep, db: DBDep, booking_id: int):
    try:
        await BookingsService(db).delete_booking(uid, booking_id)
    except ObjectNotFoundException as ex:
        raise BookingNotFoundHTTPException from ex
    except UnknownException as ex:
        raise UnknownHTTPException from ex
        
    return {"status": "OK"}

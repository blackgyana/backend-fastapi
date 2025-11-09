from datetime import date
import logging
from fastapi_cache.decorator import cache
from fastapi import Body, HTTPException, Query, APIRouter

from src.exceptions.base import UnknownException
from src.exceptions.framework import FacilitiesInBulkNotFoundHTTPException, InvalidDatesHTTPException, RoomAlreadyExistsHTTPException, RoomNotFoundHTTPException, UnknownHTTPException
from src.exceptions.repositories import ObjectAlreadyExistsException, ObjectInBulkNotFoundException, ObjectNotFoundException
from src.exceptions.services import InvalidDatesException
from src.api.dependencies import DBDep
from src.schemas.rooms import (
    RoomAddDTO,
    RoomAddRequest,
    RoomPatchRequest,
    RoomWithRels,
)
from src.services.rooms import RoomsService

router = APIRouter(prefix="/hotels")


@router.get("/{hotel_id}/rooms", summary="Получить все номера")
@cache(expire=60)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(examples=["2025-03-01"]),
    date_to: date = Query(examples=["2025-03-10"]),
) -> list[RoomWithRels]:

    try:
        return await RoomsService(db).get_rooms(hotel_id, date_from, date_to)
    except InvalidDatesException as ex:
        raise InvalidDatesHTTPException from ex
    except UnknownException as ex:
        raise UnknownHTTPException from ex 


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер")
@cache(expire=60)
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomsService(db).get_room(hotel_id, room_id)
    except ObjectNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except UnknownException as ex:
        raise UnknownHTTPException from ex


@router.post("/{hotel_id}/rooms", summary="Добавить номер")
async def add_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Одноместный",
                "value": {
                    "title": "Одноместный стандартный",
                    "description": "Одноместный, с душем, тумбой и шкафом, без завтрака",
                    "price": 3400,
                    "quantity": 2,
                    "facilities_ids": [],
                },
            },
            "2": {
                "summary": "Люкс",
                "value": {
                    "title": "Двухместный люкс",
                    "description": "Двуспальная кровать, душ, джакузи, балкон, шкаф-купе, тумбочка, необходимая техника, завтрак в кровать",
                    "price": 6400,
                    "quantity": 1,
                    "facilities_ids": [],
                },
            },
        }
    ),
):
    try:
        room = await RoomsService(db).add_room(hotel_id, room_data)
    except ObjectAlreadyExistsException as ex:
        raise RoomAlreadyExistsHTTPException from ex
    except ObjectInBulkNotFoundException as ex:
        raise FacilitiesInBulkNotFoundHTTPException from ex
    except UnknownException as ex:
        raise UnknownHTTPException from ex
    
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновить информацию о номере",
    description="Обновлять привязку к отелю hotel_id нельзя",
)
async def update_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    try:
        room = await RoomsService(db).update_room(hotel_id, room_id, room_data)
    except ObjectNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except ObjectInBulkNotFoundException as ex:
        raise FacilitiesInBulkNotFoundHTTPException from ex
    except UnknownException as ex:
        raise UnknownHTTPException from ex
    return {"status": "OK", 'data': room}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частично обновить информацию о номере",
    description="Обновлять привязку к отелю hotel_id нельзя",
)
async def update_room_part(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    try:
        room = await RoomsService(db).update_room_part(hotel_id, room_id, room_data)
    except ObjectNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except ObjectInBulkNotFoundException as ex:
        raise FacilitiesInBulkNotFoundHTTPException from ex
    except UnknownException as ex:
        raise UnknownHTTPException from ex
    return {"status": "OK", 'data': room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomsService(db).delete_room(hotel_id, room_id)
    except ObjectNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except UnknownException as ex:
        raise UnknownHTTPException from ex
    return {"status": "OK"}

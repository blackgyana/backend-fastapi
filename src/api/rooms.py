from datetime import date
from fastapi_cache.decorator import cache
from fastapi import Body, HTTPException, Query, APIRouter

from src.exceptions.base import ObjectAlreadyExistsException, ObjectInBulkNotFoundException, ObjectNotFoundException, UnknownException
from src.schemas.facilities import RoomsFacilitiesAdd
from src.api.dependencies import DBDep
from src.schemas.rooms import (
    RoomDTO,
    RoomAddDTO,
    RoomAddRequest,
    RoomPatch,
    RoomPatchRequest,
    RoomWithRels,
)

router = APIRouter(prefix="/hotels")


@router.get("/{hotel_id}/rooms", summary="Получить все номера")
@cache(expire=60)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(examples=["2025-03-01"]),
    date_to: date = Query(examples=["2025-03-10"]),
) -> list[RoomWithRels]:

    if date_from >= date_to:
        raise HTTPException(status_code=400, detail='Дата въезда не может быть позже даты выезда')


    return await db.rooms.get_filtered_by_dates(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер")
@cache(expire=60)
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await db.rooms.get_one(hotel_id=hotel_id, room_id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail='Номер не найден')


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
    
    _room_data = RoomAddDTO(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room: RoomDTO = await db.rooms.add(_room_data)
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409, detail='Номер уже существует')
    rooms_facilities_data = [
        RoomsFacilitiesAdd(room_id=room.id, facility_id=fid) for fid in set(room_data.facilities_ids)
    ]
    try:
        if rooms_facilities_data:
            await db.rooms_facilities.add_bulk(rooms_facilities_data)
        await db.commit()
    except ObjectInBulkNotFoundException:
        raise HTTPException(status_code=409, detail='Некоторые объекты не найдены в списке удобств')
    except UnknownException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновить информацию о номере",
    description="Обновлять привязку к отелю hotel_id нельзя",
)
async def update_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAddDTO(**room_data.model_dump(), hotel_id=hotel_id)
    try:
        await db.rooms.update(_room_data, id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail='Номер не найден')
    try:
        await db.rooms_facilities.set(room_id=room_id, facilities_ids=room_data.facilities_ids)
        await db.commit()
    except ObjectInBulkNotFoundException:
        raise HTTPException(status_code=409, detail='Некоторые объекты не найдены в списке удобств')
    except UnknownException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частично обновить информацию о номере",
    description="Обновлять привязку к отелю hotel_id нельзя",
)
async def update_room_part(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    clear_data = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(**clear_data, hotel_id=hotel_id)
    try:
        await db.rooms.update(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in clear_data:
            await db.rooms_facilities.set(room_id=room_id, facilities_ids=room_data.facilities_ids)
    
        await db.commit()
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail='Номер не найден')
    except ObjectInBulkNotFoundException:
        raise HTTPException(status_code=409, detail='Некоторые объекты не найдены в списке удобств')
    except UnknownException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await db.commit()
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail='Номер не найден')
    except UnknownException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    return {"status": "OK"}

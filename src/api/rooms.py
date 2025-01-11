from datetime import date
from fastapi import Body, Query, APIRouter
from src.schemas.facilities import RoomsFacilitiesAdd
from src.api.dependencies import DBDep
from src.schemas.rooms import Room, RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix='/hotels')


@router.get("/{hotel_id}/rooms", summary='Получить все номера')
async def get_rooms(db: DBDep, 
                    hotel_id: int,
                    date_from: date = Query(example='2025-03-01'),
                    date_to: date = Query(example='2025-03-10')
                    ) -> list[Room]:
    return await db.rooms.get_filtered_by_dates(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get('/{hotel_id}/rooms/{room_id}', summary='Получить 1 номер')
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary='Добавить номер')
async def add_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    '1': {'summary': 'Одноместный', 'value': {
        'title': 'Одноместный стандартный',
        'description': 'Одноместный, с душем, тумбой и шкафом, без завтрака',
        'price': 3400,
        'quantity': 2,
        'facilities_ids': []
    }},
    '2': {'summary': 'Люкс', 'value': {
        'title': 'Двухместный люкс',
        'description': 'Двуспальная кровать, душ, джакузи, балкон, шкаф-купе, тумбочка, необходимая техника, завтрак в кровать',
        'price': 6400,
        'quantity': 1,
        'facilities_ids': []
    }}
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room: Room = await db.rooms.add(_room_data)
    rooms_facilities_data = [RoomsFacilitiesAdd(room_id=room.id, facility_id=fid) for fid in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {'status': 'OK', 'data': room}


@router.put("/{hotel_id}/rooms/{room_id}", summary='Обновить информацию о номере', 
            description='Обновлять привязку к отелю hotel_id нельзя')
async def update_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(**room_data.model_dump(exclude='facilities_ids'), hotel_id=hotel_id)
    await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.set(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}/rooms/{room_id}", summary='Частично обновить информацию о номере', 
              description='Обновлять привязку к отелю hotel_id нельзя')
async def update_room_part(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(**room_data.model_dump(exclude='facilities_ids', exclude_unset=True), hotel_id=hotel_id)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.set(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {'status': 'OK'}


@router.delete("/{hotel_id}/rooms/{room_id}", summary='Удалить номер')
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {'status': 'OK'}

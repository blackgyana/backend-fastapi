from fastapi import Body, Query, APIRouter
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.database import async_session_maker

router = APIRouter(prefix='/hotels')


@router.get("/{hotel_id}/rooms", summary='Получить все номера')
async def get_rooms(hotel_id: int) -> list[Room]:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get('/{hotel_id}/rooms/{room_id}', summary='Получить 1 номер')
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary='Добавить номер')
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    '1': {'summary': 'Одноместный', 'value': {
        'title': 'Одноместный стандартный',
        'description': 'Одноместный, с душем, тумбой и шкафом, без завтрака',
        'price': 3400,
        'quantity': 2
    }},
    '2': {'summary': 'Люкс', 'value': {
        'title': 'Двухместный люкс',
        'description': 'Двуспальная кровать, душ, джакузи, балкон, шкаф-купе, тумбочка, необходимая техника, завтрак в кровать',
        'price': 6400,
        'quantity': 1
    }}
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        new_room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {'status': 'OK', 'data': new_room}


@router.put("/{hotel_id}/rooms/{room_id}", summary='Обновить информацию о номере', description='Обновлять привязку к отелю hotel_id нельзя')
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}/rooms/{room_id}", summary='Частично обновить информацию о номере', description='Обновлять привязку к отелю hotel_id нельзя')
async def update_room_part(hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.delete("/{hotel_id}/rooms/{room_id}", summary='Удалить номер')
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}

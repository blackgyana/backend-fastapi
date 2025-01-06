from fastapi import Body, Query, APIRouter
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker

router = APIRouter(prefix='/hotels')


@router.get("/{hotel_id}/rooms", summary='Получить все номера')
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description='Название номера'),
    description: str | None = Query(None, description='Описание номера')
) -> list[Room]:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            title=title,
            description=description,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1)
        )


@router.get('/{hotel_id}/rooms/{room_id}', summary='Получить 1 номер')
async def get_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary='Добавить номер')
async def create_hotel(hotel_id: int, room_data: RoomAdd = Body(openapi_examples={
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
    room_data.hotel_id = hotel_id
    async with async_session_maker() as session:
        new_hotel = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {'status': 'OK', 'data': new_hotel}


@router.put("/{hotel_id}/rooms/{room_id}", summary='Обновить информацию о номере')
async def update_hotel(hotel_id: int, room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}/rooms/{room_id}", summary='Частично обновить информацию о номере')
async def update_hotel_part(hotel_id: int, room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.delete("/{hotel_id}/rooms/{room_id}", summary='Удалить номер')
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}

from fastapi import Body, Query, APIRouter
from sqlalchemy import insert
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker

router = APIRouter(prefix='/hotels')


@router.get("", summary='Получить все отели')
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description='Название отеля'),
    location: str | None = Query(None, description='Расположение отеля')
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1)
        )


@router.post("", summary='Добавить отель')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value': {
        'title': 'Русь 5 звезд',
        'location': 'Сочи, ул. Морская, 3'
    }},
    '2': {'summary': 'Калининград', 'value': {
        'title': 'Estate премиум люкс',
        'location': 'Калининград, ул. Набережная, 5'
    }}
})):
    async with async_session_maker() as session:
        new_hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {'status': 'OK', 'data': new_hotel}


@router.put("/{hotel_id}", summary='Обновить информацию об отеле')
async def update_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}", summary='Частично обновить информацию об отеле', description='Можно менять каждое поле в отдельности или все поля разом')
def update_hotel_part(hotel_id: int, hotel: HotelPATCH):
    hotel = next((h for h in hotels if h['id'] == hotel_id), None)
    if not hotel:
        return {'message': 'Not found'}
    hotel['title'] = hotel.title if hotel.title is not None else hotel['title']
    hotel['name'] = hotel.name if hotel.name is not None else hotel['name']
    return {'message': 'OK'}


@router.delete("/{hotel_id}", summary='Удалить отель')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}

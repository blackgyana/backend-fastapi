from datetime import date
from fastapi import Body, Query, APIRouter
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH
from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix='/hotels')


@router.get("", summary='Получить все отели')
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(example='2025-03-01'),
    date_to: date = Query(example='2025-03-10'),
    title: str | None = Query(None, description='Название отеля'),
    location: str | None = Query(None, description='Расположение отеля')
) -> list[Hotel]:

    limit = pagination.per_page
    offset = pagination.per_page * (pagination.page - 1)

    return await db.hotels.get_filtered_by_dates(
        date_from=date_from, 
        date_to=date_to, 
        limit=limit, 
        offset=offset, 
        title=title, 
        location=location)


@router.get('/{hotel_id}', summary='Получить 1 отель')
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary='Добавить отель')
async def add_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value': {
        'title': 'Русь 5 звезд',
        'location': 'Сочи, ул. Морская, 3'
    }},
    '2': {'summary': 'Калининград', 'value': {
        'title': 'Estate премиум люкс',
        'location': 'Калининград, ул. Набережная, 5'
    }}
})):
    new_hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {'status': 'OK', 'data': new_hotel}


@router.put("/{hotel_id}", summary='Обновить информацию об отеле')
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}", summary='Частично обновить информацию об отеле', description='Можно менять каждое поле в отдельности или все поля разом')
async def update_hotel_part(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.delete("/{hotel_id}", summary='Удалить отель')
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status': 'OK'}

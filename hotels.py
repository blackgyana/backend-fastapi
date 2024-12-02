from fastapi import Body, Query, APIRouter
from pydantic import BaseModel, Field
from schemas.hotels import Hotel, HotelPATCH
from dependencies import PaginationDep

router = APIRouter(prefix='/hotels')


hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Дубай', 'name': 'dubai'},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("", summary='Получить все отели')
def get_hotels(
    pagination: PaginationDep,
    hotel_id: int | None = Query(None, description='id отеля'),
    title: str | None = Query(None, description='Название отеля'),
    
):
    result = [hotel for hotel in hotels if hotel_id and hotel_id ==
              hotel['id'] or title and title in hotel['title']] or hotels
    return result[(pagination.page - 1) * pagination.per_page:pagination.page * pagination.per_page]


@router.post("", summary='Добавить отель')
def create_hotel(hotel: Hotel = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value': {
        'title': 'Сочи 5 звезд у моря',
        'name': 'sochi_u_morya'
    }},
    '2': {'summary': 'Калининград', 'value': {
        'title': 'Калининград премиум люкс',
        'name': 'kaliningrad_premium_lux'
    }}
})):
    hotels.append({
        'id': hotels[-1]['id']+1,
        'title': hotel.title,
        'name': hotel.name
    })
    return {'message': 'OK'}


@router.put("/{hotel_id}", summary='Обновить информацию об отеле')
def update_hotel(hotel_id: int, hotel: Hotel):
    hotel = next((h for h in hotels if h['id'] == hotel_id), None)
    if not hotel:
        return {'message': 'Not found'}
    hotel['title'] = hotel.title
    hotel['name'] = hotel.name
    return {'message': 'OK'}


@router.patch("/{hotel_id}", summary='Частично обновить информацию об отеле', description='Можно менять каждое поле в отдельности или все поля разом')
def update_hotel_part(hotel_id: int, hotel: HotelPATCH):
    hotel = next((h for h in hotels if h['id'] == hotel_id), None)
    if not hotel:
        return {'message': 'Not found'}
    hotel['title'] = hotel.title if hotel.title is not None else hotel['title']
    hotel['name'] = hotel.name if hotel.name is not None else hotel['name']
    return {'message': 'OK'}


@router.delete("/{hotel_id}", summary='Удалить отель')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'message': 'OK'}

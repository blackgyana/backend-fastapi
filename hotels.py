from fastapi import Body, Query, APIRouter

router = APIRouter(prefix='/hotels')


hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Дубай', 'name': 'dubai'}
]


@router.get("", summary='Получить все отели')
def get_hotels(hotel_id: int | None = Query(None, description='id отеля'), 
               title: str | None = Query(None, description='Название отеля')):
    result = [hotel for hotel in hotels if hotel_id and hotel_id == hotel['id'] \
              or title and title in hotel['title']] or hotels
    return result


@router.post("", summary='Добавить отель')
def create_hotel(title: str = Body(), name: str = Body()):
    hotels.append({
        'id': hotels[-1]['id']+1,
        'title': title,
        'name': name
    })
    return {'message': 'OK'}


@router.put("/{hotel_id}", summary='Обновить информацию об отеле')
def update_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    hotel = next((h for h in hotels if h['id'] == hotel_id), None)
    if not hotel:
        return {'message': 'Not found'}
    hotel['title'] = title
    hotel['name'] = name
    return {'message': 'OK'}


@router.patch("/{hotel_id}", summary='Частично обновить информацию об отеле', description='Можно менять каждое поле в отдельности или все поля разом')
def update_hotel_part(hotel_id: int, title: str | None = Body(None), name: str | None = Body(None)):
    hotel = next((h for h in hotels if h['id'] == hotel_id), None)
    if not hotel:
        return {'message': 'Not found'}
    hotel['title'] = title if title is not None else hotel['title']
    hotel['name'] = name if name is not None else hotel['name']
    return {'message': 'OK'}


@router.delete("/{hotel_id}", summary='Удалить отель')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'message': 'OK'}

from fastapi import Body, FastAPI
import uvicorn

app = FastAPI()


hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Дубай', 'name': 'dubai'}
]


@app.get("/hotels", description='Получить все отели')
def get_hotels():
    return hotels


@app.post("/hotels", description='Добавить отель')
def create_hotel(title: str = Body(), name: str = Body()):
    hotels.append({
        'id': hotels[-1]['id']+1,
        'title': title,
        'name': name
    })
    return {'message': 'OK'}


@app.put("/hotels/{hotel_id}", description='Обновить информацию об отеле')
def update_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    hotel = next((h for h in hotels if h['id'] == hotel_id), None)
    if not hotel:
        return {'message': 'Not found'}
    hotel['title'] = title
    hotel['name'] = name
    return {'message': 'OK'}


@app.patch("/hotels/{hotel_id}", description='Частично обновить информацию об отеле')
def update_hotel_part(hotel_id: int, title: str | None = Body(None), name: str | None = Body(None)):
    hotel = next((h for h in hotels if h['id'] == hotel_id), None)
    if not hotel:
        return {'message': 'Not found'}
    hotel['title'] = title or hotel['title']
    hotel['name'] = name or hotel['name']
    return {'message': 'OK'}


@app.delete("/hotels/{hotel_id}", description='Удалить отель')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'message': 'OK'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

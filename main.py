from fastapi import Body, FastAPI
import uvicorn

app = FastAPI()


hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Дубай', 'name': 'dubai'}
]


@app.get("/hotels")
def get_hotels():
    return hotels


@app.post("/hotels")
def create_hotel(title: str = Body(), name: str = Body()):
    hotels.append({
        'id': hotels[-1]['id']+1,
        'title': title,
        'name': name
    })
    return {'message': 'OK'}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'message': 'OK'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

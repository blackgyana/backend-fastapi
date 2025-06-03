from httpx import AsyncClient

from src.utils.db_manager import DBManager


async def test_add_booking(authenticated_http: AsyncClient, db: DBManager):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_http.post(
        url='/bookings',
        json={
            'room_id': room_id,
            'date_from':'2025-05-20',
            'date_to':'2025-05-24',
        }
    )
    res = response.json()
    assert response.status_code == 200
    assert 'status' in res and res['status'] == 'OK'
    assert 'data' in res and res['data']
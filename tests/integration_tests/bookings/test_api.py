import pytest
from httpx import AsyncClient
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool

@pytest.mark.parametrize('room_id, hotel_id, date_from, date_to, status_code',[
    (1, 1, '2025-05-20', '2025-05-20', 400),
    (1, 1, '2025-05-20', '2025-05-26', 200),
    (1, 1, '2025-05-21', '2025-05-27', 200),
    (1, 1, '2025-05-22', '2025-05-28', 200),
    (1, 1, '2025-05-23', '2025-05-29', 200),
    (1, 1, '2025-05-24', '2025-05-30', 200),
    (1, 1, '2025-05-25', '2025-05-31', 400),
])
async def test_add_booking(
    room_id, hotel_id, date_from, date_to, status_code,
    authenticated_http: AsyncClient):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_http.post(
        url='/bookings',
        json={
            'room_id': room_id,
            'hotel_id': hotel_id,
            'date_from':date_from,
            'date_to':date_to,
        }
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        res = response.json()
        assert 'status' in res and res['status'] == 'OK'
        assert 'data' in res and res['data']


@pytest.fixture(scope='module')
async def test_clear_bookings():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.bookings.delete()
        await db.commit()


@pytest.mark.parametrize('room_id, hotel_id, date_from, date_to, status_code, bookings_count',[
    (1, 1, '2025-05-20', '2025-05-26', 200, 1),
    (1, 1, '2025-05-21', '2025-05-27', 200, 2),
    (1, 1, '2025-05-22', '2025-05-28', 200, 3),
])
async def test_add_and_get_bookings(
    room_id, hotel_id, date_from, date_to, status_code, bookings_count,
    authenticated_http: AsyncClient, test_clear_bookings):

    await test_add_booking(room_id, hotel_id, date_from, date_to, status_code, authenticated_http)
    response = await authenticated_http.get(
        url='/bookings/me'
    )
    assert response.status_code == 200
    res = response.json()
    assert len(res) == bookings_count


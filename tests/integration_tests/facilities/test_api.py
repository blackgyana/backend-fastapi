from httpx import AsyncClient


async def test_add_facility(http: AsyncClient):
    response = await http.post(
        url='/facilities',
        json={
            'title': 'Удобство 1'
        }
    )

    assert response.status_code == 200

async def test_get_facilities(http:AsyncClient):
    response = await http.get(
        url='/facilities'
    )

    assert response.status_code == 200


from httpx import AsyncClient


async def test_get_hotels(http: AsyncClient):
    response = await http.get(
        url="/hotels",
        params={
            "date_from": "2025-05-20",
            "date_to": "2025-05-24",
        },
    )
    print(f"{response.json()=}")
    assert response.status_code == 200

from httpx import AsyncClient


async def test_add_facility(http: AsyncClient):
    title = "Удобство"
    response = await http.post(url="/facilities", json={"title": title})
    res = response.json()
    print(f"{res=}")
    assert response.status_code == 200
    assert res["status"] == "OK"
    assert "data" in res
    assert res["data"]["title"] == title


async def test_get_facilities(http: AsyncClient):
    response = await http.get(url="/facilities")

    assert response.status_code == 200

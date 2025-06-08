from httpx import AsyncClient

email = "user_test@mail.ru"
password = "1234Pass"


async def test_auth_user_flow(http: AsyncClient):
    user_credentials = {"email": email, "password": password}
    response = await http.post(url="/auth/register", json=user_credentials)
    assert response.status_code == 200
    if response.status_code > 200:
        return

    response = await http.post(url="/auth/login", json=user_credentials)
    assert response.status_code == 200
    res = response.json()
    assert "access_token" in http.cookies and "access_token" in res

    response = await http.get(url="/auth/me")
    assert response.status_code == 200
    res = response.json()
    assert "email" in res and res["email"] == user_credentials["email"]
    assert "password" not in res
    assert "hashed_password" not in res

    response = await http.post(url="/auth/logout")
    assert response.status_code == 200
    res = response.json()
    assert "status" in res and res["status"] == "OK"
    assert "access_token" not in http.cookies

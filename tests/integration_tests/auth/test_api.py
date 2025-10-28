from httpx import AsyncClient
import pytest

# email = "user_test@mail.ru"
# password = "1234Pass"

@pytest.mark.parametrize(
        "email, password, status_code",
        [
            ('test@mail.ru', 'SomePass231', 200),
            ('test@mail.ru', 'SomePass231', 409),
            ('user_test@mail.ru', '1234Pass', 200),
            ('qwerty@mail.com', 'JB#r5k345', 200)
        ]
)
async def test_auth_user_flow(email:str, password:str, status_code: str, http: AsyncClient):
    user_credentials = {"email": email, "password": password}
    response = await http.post(url="/auth/register", json=user_credentials)
    assert response.status_code == status_code
    if response.status_code != 200:
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

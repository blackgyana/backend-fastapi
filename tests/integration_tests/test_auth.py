from src.services.auth import AuthService


def test_encode_decode_access_token():
    data = {"user_id": 1}
    jwt = AuthService().create_access_token(data)

    assert jwt
    assert isinstance(jwt, str)

    payload = AuthService().decode_token(jwt)
    assert payload["user_id"] == data["user_id"]

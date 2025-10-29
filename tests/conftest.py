from unittest.mock import patch
from typing import AsyncGenerator
import json

# @cache mock
patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()


import pytest
from src.api.dependencies import get_db
from src.schemas.hotels import HotelAddDTO
from src.schemas.rooms import RoomAddDTO
from src.database import Base, engine_null_pool
from src.models import *
from src.config import settings
from src.main import app
from src.database import async_session_maker_null_pool
from src.utils.db_manager import DBManager


from httpx import ASGITransport, AsyncClient


# Подготавливаем среду тестирования


@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST" and settings.DB_NAME == "test"


# Для 1 единственного соединения с БД на каждую тест-функцию (без пула)
async def db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

# Фикстура для передачи в bookings/test_db
@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in db_null_pool():
        yield db

# Перезаписываем dependency приложения на время запуска тестов через 1 соединение
@pytest.fixture(scope="function", autouse=True)
async def override_get_db() -> AsyncGenerator[DBManager, None]:
    app.dependency_overrides[get_db] = db_null_pool
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        print('=== БД готова к выполнению тестов! ===')

@pytest.fixture(scope="session", autouse=True)
async def load_mock_data(setup_database):
    with open("tests/mock_hotels.json", "r", encoding="utf-8") as f:
        hotels_data = json.load(f)
    with open("tests/mock_rooms.json", "r", encoding="utf-8") as f:
        rooms_data = json.load(f)
    hotels = [HotelAddDTO(**h) for h in hotels_data]
    rooms = [RoomAddDTO(**r) for r in rooms_data]
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()

# scope = session - на сессию тестирования
# scope = function - на 1 вызов функции

@pytest.fixture
async def http() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
        yield http


@pytest.fixture(scope="session")
async def http_session() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http_client:
        yield http_client



user_auth_data = {"email": "test@mail.com", "password": "pass1234"}


@pytest.fixture(scope="session", autouse=True)
async def register_user(http_session: AsyncClient, load_mock_data):
    'Создать пользователя после загрузки мок-данных'
    await http_session.post(url="/auth/register", json=user_auth_data)


@pytest.fixture(scope="session")
async def authenticated_http(http_session: AsyncClient, register_user):
    'Аутентификация созданного пользователя и возврат http-клиента с полученными cookie'
    response = await http_session.post(url="/auth/login", json=user_auth_data)
    res = response.json()
    assert response.status_code == 200
    assert "access_token" in res
    assert http_session.cookies.get("access_token")
    yield http_session

from typing import AsyncGenerator
import pytest
from src.schemas.hotels import HotelAddDTO
from src.schemas.rooms import RoomAddDTO
from src.database import Base, engine_null_pool
from src.models import *
from src.config import settings
from src.main import app
from src.database import async_session_maker_null_pool
from src.utils.db_manager import DBManager
import json

from httpx import ASGITransport, AsyncClient


# Подготавливаем среду тестирования

@pytest.fixture(scope='session', autouse=True)
async def check_mode():
    assert settings.MODE == 'TEST' and settings.DB_NAME == 'test'


@pytest.fixture()
async def db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope='session')
async def http() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as http:
        yield http


@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope='session', autouse=True)
async def load_mock_data(setup_database):
    with open('tests/mock_hotels.json', 'r', encoding='utf-8') as f:
        hotels_data = json.load(f)
    with open('tests/mock_rooms.json', 'r', encoding='utf-8') as f:
        rooms_data = json.load(f)
    hotels = [HotelAddDTO(**h) for h in hotels_data]
    rooms = [RoomAddDTO(**r) for r in rooms_data]
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()


@pytest.fixture(scope='session', autouse=True)
async def create_user(load_mock_data, http: AsyncClient):
    await http.post(
        url='/auth/register',
        json={
            'email': 'test@mail.com',
            'password': 'pass1234'
        })
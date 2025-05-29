import pytest
from src.database import Base, engine_null_pool
from src.models import *
from src.config import settings
from src.main import app

from httpx import ASGITransport, AsyncClient


# Подготавливаем среду тестирования

@pytest.fixture(scope='session', autouse=True)
async def check_mode():
    assert settings.MODE == 'TEST' and settings.DB_NAME == 'test'

@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_mode):
    async with engine_null_pool.begin() as conn:
        print('=== REFRESH DATABASE ===')
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

@pytest.fixture(scope='session', autouse=True)
async def create_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app)) as http:
        http.post(
            url='/auth/register',
            json={
                'email': 'test@mail.com',
                'password': 'pass1234'
            })
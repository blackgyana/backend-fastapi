import logging
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import settings


engine = create_async_engine(settings.DB_URL)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)

# session = async_session_maker()

async def check_database_connection():
    """Простая проверка подключения к БД"""
    try:
        logging.info('Проверяем подключение к БД ....')
        async with async_session_maker_null_pool() as session:
            # Просто выполняем простой запрос
            await session.execute(text("SELECT 1"))
        logging.info("✅ Успешное подключение к БД")
    except Exception as e:
        logging.error(f"❌ Ошибка подключения к БД: {e}")
        raise

class Base(DeclarativeBase):
    pass

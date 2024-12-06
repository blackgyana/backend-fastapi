from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings


engine = create_async_engine(settings.DB_URL)


# import asyncio
# RAW SQL
# async def raw_func():
#     async with engine.begin() as conn:
#         res = await conn.execute(text('SELECT version()'))
#         print(res.fetchone())

# asyncio.run(raw_func())
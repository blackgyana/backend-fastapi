import asyncio
import logging
from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend



sys.path.append(str(Path(__file__).parent.parent))

# from src.tasks.tasks import periodic_loop_task
from src.api.images import router as images_router
from src.api.facilities import router as facilities_router
from src.api.bookings import router as bookings_router
from src.api.rooms import router as rooms_router
from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.init import redis_manager
from src.config import settings
from src.database import check_database_connection

logging.basicConfig(level=logging.INFO)


# Функция для управления жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск бесконечных фоновых задач в цикле 
    # asyncio.create_task(periodic_loop_task())
    # Инициализация RedisManager при запуске приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis_client), prefix="fastapi-cache")
    # Проверка подключения к БД
    await check_database_connection()
    yield
    # Закрытие RedisManager при остановке приложения
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router, tags=["Авторизация"])
app.include_router(hotels_router, tags=["Отели"])
app.include_router(rooms_router, tags=["Номера"])
app.include_router(bookings_router, tags=["Бронирования"])
app.include_router(facilities_router, tags=["Удобства"])
app.include_router(images_router, tags=['Изображения отелей'])


# Получаем текущую схему OpenAPI
openapi_schema = app.openapi()
# Добавляем новую security scheme для куки авторизации
openapi_schema["components"]["securitySchemes"] = {
    "CookieAuth": {
        "type": "apiKey",
        "in": "cookie",  # Указываем, что это cookie
        "name": settings.COOKIE_NAME,  # Название куки, которая будет содержать токен
    }
}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

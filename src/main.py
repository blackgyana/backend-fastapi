
from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

from src.api.facilities import router as facilities_router
from src.api.bookings import router as bookings_router
from src.api.rooms import router as rooms_router
from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.init import redis_manager
from src.config import settings



# Функция для управления жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация RedisManager при запуске приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(
        redis_manager.redis_client), prefix='fastapi-cache')
    yield
    # Закрытие RedisManager при остановке приложения
    await redis_manager.close()


app = FastAPI()


app.include_router(auth_router, tags=['Авторизация'])
app.include_router(hotels_router, tags=['Отели'])
app.include_router(rooms_router, tags=['Номера'])
app.include_router(bookings_router, tags=['Бронирования'])
app.include_router(facilities_router, tags=['Удобства'])


# Получаем текущую схему OpenAPI
openapi_schema = app.openapi()
# Добавляем новую security scheme для куки авторизации
openapi_schema["components"]['securitySchemes']={
        'CookieAuth': {
            "type": "apiKey",
            "in": "cookie",  # Указываем, что это cookie
            "name": settings.COOKIE_NAME  # Название куки, которая будет содержать токен
        }
    }



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

from redis.asyncio import Redis
from typing import AsyncGenerator

class RedisManager:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: str|None = None):
        # Параметры подключения
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        # Клиент Redis (инициализируется в методе connect)
        self.redis_client: Redis|None = None

    async def connect(self):
        """Устанавливает соединение с Redis."""
        if self.redis_client is None:
            self.redis_client = Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True
            )

    async def _ensure_connected(self):
        """Проверяет, что клиент Redis подключен."""
        if self.redis_client is None:
            raise RuntimeError("Redis client is not connected")

    async def set(self, key: str, value: str) -> bool:
        """Устанавливает значение по ключу."""
        await self._ensure_connected()
        return await self.redis_client.set(key, value)

    async def get(self, key: str) -> str|None:
        """Получает значение по ключу."""
        await self._ensure_connected()
        return await self.redis_client.get(key)

    async def delete(self, key: str) -> int:
        """Удаляет значение по ключу."""
        await self._ensure_connected()
        return await self.redis_client.delete(key)

    async def close(self):
        """Закрывает соединение с Redis."""
        if self.redis_client is not None:
            await self.redis_client.close()
            self.redis_client = None

# Зависимость Depends для использования в FastAPI
async def get_redis_manager() -> AsyncGenerator[RedisManager, None]:
    redis_manager = RedisManager()
    try:
        await redis_manager.connect()  # Устанавливаем соединение
        yield redis_manager
    finally:
        await redis_manager.close()  # Закрываем соединение
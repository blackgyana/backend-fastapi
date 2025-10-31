

# Исключения на уровне сервиса 
# (уточнение основных исключений из репозиториев)

from src.exceptions.base import UnknownException


class FreeRoomsNotFoundException(UnknownException):
    detail = 'Нет свободных номеров'

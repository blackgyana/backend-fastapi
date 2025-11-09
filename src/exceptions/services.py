

# Исключения на уровне сервиса 
# (уточнение основных исключений из репозиториев)

from src.exceptions.base import UnknownException


class FreeRoomsNotFoundException(UnknownException):
    detail = 'Нет свободных номеров'

class RoomNotFoundException(UnknownException):
    detail = 'Номер не найден'

class HotelNotFoundException(UnknownException):
    detail = 'Отель не найден'

class InvalidDatesException(UnknownException):
    detail = 'Неверно указаны даты'
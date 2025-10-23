
from src.database import Base


class UnknownException(Exception):
    detail = 'Неизвестная ошибка'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(UnknownException):
    detail = 'Объект не найден'

class FreeRoomsNotFoundException(UnknownException):
    detail = 'Нет свободных номеров'

class ObjectAlreadyExistsException(UnknownException):
    detail = 'Объект уже существует'
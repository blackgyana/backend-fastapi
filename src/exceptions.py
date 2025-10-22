
from src.database import Base


class BaseException(Exception):
    detail = 'Неизвестная ошибка'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(BaseException):
    detail = 'Объект не найден'

class NoFreeRoomsException(BaseException):
    detail = 'Нет свободных номеров'
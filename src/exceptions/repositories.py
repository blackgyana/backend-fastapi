
# Исключения на уровне репозитория 

from src.exceptions.base import UnknownException


class ObjectNotFoundException(UnknownException):
    detail = 'Объект не найден'

class ObjectAlreadyExistsException(UnknownException):
    detail = 'Объект уже существует'

class ObjectInBulkNotFoundException(UnknownException):
    detail = 'Объект в списке не найден'

# Исключения на уровне фреймворка
# Для FastAPI - это HTTPException 
from fastapi import HTTPException

class UnknownHTTPException(HTTPException):
    status_code=500
    detail = 'Неизвестная ошибка на сервере'

    # не забываем переопределить init 
    def __init__(self, status_code:int | None = None, detail: str | None = None):
        super().__init__(status_code=status_code or self.status_code, detail=detail or self.detail)


class InvalidDatesHTTPException(UnknownHTTPException):
    status_code=400
    detail = 'Дата въезда не может быть позже даты выезда'

class FacilitiesInBulkNotFoundHTTPException(UnknownHTTPException):
    status_code = 409
    detail = 'Некоторые удобства из списка не найдены'
    
class HotelNotFoundHTTPException(UnknownHTTPException):
    status_code = 404
    detail = 'Отель не найден'

class HotelAlreadyExistsHTTPException(UnknownHTTPException):
    status_code = 409
    detail = 'Отель уже существует'

class RoomNotFoundHTTPException(UnknownHTTPException):
    status_code = 404
    detail = 'Номер не найден'

class RoomAlreadyExistsHTTPException(UnknownHTTPException):
    status_code = 409
    detail = 'Номер уже существует'

class FacilityAlreadyExistsHTTPException(UnknownHTTPException):
    status_code = 409
    detail = 'Удобство уже существует'

class BookingNotFoundHTTPException(UnknownHTTPException):
    status_code = 404
    detail = 'Бронирование не найдено'

class FreeRoomsNotFoundHTTPException(UnknownHTTPException):
    status_code = 409
    detail = 'Нет свободных номеров'


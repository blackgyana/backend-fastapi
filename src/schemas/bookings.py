from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BookingAddRequest):
    user_id: int
    price: int


class BookingDTO(BookingAdd):
    id: int
    total_cost: int
    created_at: datetime

    # приводить к pydantic схеме из атрибутов ORM модели и не принимать лишние поля
    # model_config = ConfigDict(from_attributes=True, extra='forbid')

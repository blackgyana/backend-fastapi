from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class BookingsAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingsAdd(BookingsAddRequest):
    user_id: int
    price: int


class Bookings(BookingsAdd):
    id: int
    total_cost: int
    created_at: datetime

    # приводить к pydantic схеме из атрибутов ORM модели и не принимать лишние поля
    model_config = ConfigDict(from_attributes=True, extra='forbid')

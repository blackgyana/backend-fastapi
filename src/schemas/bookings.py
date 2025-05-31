from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddDTO(BookingAddRequest):
    user_id: int
    price: int

class BookingUpdateDTO(BaseModel):
    user_id: int = None
    room_id: int  = None
    date_from: date  = None
    date_to: date  = None
    price: int  = None


class BookingDTO(BookingAddDTO):
    id: int
    total_cost: int
    created_at: datetime


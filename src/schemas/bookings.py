from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class BookingAddRequest(BaseModel):
    hotel_id: int
    room_id: int
    date_from: date
    date_to: date


class BookingAddDTO(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
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


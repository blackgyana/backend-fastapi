
from pydantic import BaseModel


class Room(BaseModel):
    hotel_id: int 
    title: str
    description: str | None
    price: int
    quantity: int



class RoomPATCH(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
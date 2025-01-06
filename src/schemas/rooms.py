
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict


class RoomAdd(BaseModel):
    hotel_id: int | None = None
    title: str
    description: str | None
    price: int
    quantity: int

class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True, extra='forbid')



class RoomPATCH(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
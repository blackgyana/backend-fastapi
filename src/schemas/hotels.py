from pydantic import BaseModel, Field


class HotelAddDTO(BaseModel):
    title: str
    location: str


class HotelDTO(HotelAddDTO):
    id: int


class HotelUpdateDTO(BaseModel):
    title: str | None = None
    location: str | None = None

from pydantic import BaseModel, Field


class HotelAddDTO(BaseModel):
    title: str
    location: str


class HotelDTO(HotelAddDTO):
    id: int


class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = None

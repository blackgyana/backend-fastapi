
from pydantic import BaseModel, ConfigDict


class FacilityAddDTO(BaseModel):
    title: str


class FacilityDTO(FacilityAddDTO):
    id: int



class RoomsFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacilitiesDTO(RoomsFacilitiesAdd):
    id: int

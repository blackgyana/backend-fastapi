
from pydantic import BaseModel, ConfigDict


class FacilityAdd(BaseModel):
    title: str


class FacilityDTO(FacilityAdd):
    id: int



class RoomsFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacilitiesDTO(RoomsFacilitiesAdd):
    id: int

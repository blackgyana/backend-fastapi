from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.bookings import BookingDTO
from src.schemas.facilities import FacilityDTO, RoomsFacilitiesDTO
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.schemas.rooms import RoomDTO, RoomWithRels
from src.schemas.users import UserDTO, UserWithHashedPasswordDTO
from src.schemas.hotels import HotelDTO
from src.models.hotels import HotelsORM
from src.repositories.mappers.base import DataMapper


class HotelsDataMapper(DataMapper):
    db_model = HotelsORM
    schema = HotelDTO


class RoomsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomDTO

class RoomsWithRelsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels


class UsersDataMapper(DataMapper):
    db_model = UsersORM
    schema = UserDTO


class UserWithHashedPasswordDataMapper(DataMapper):
    db_model = UsersORM
    schema = UserWithHashedPasswordDTO


class BookingsDataMapper(DataMapper):
    db_model = BookingsORM
    schema = BookingDTO


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = FacilityDTO


class RoomsFacilitiesDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schema = RoomsFacilitiesDTO

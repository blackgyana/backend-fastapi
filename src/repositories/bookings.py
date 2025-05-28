from src.repositories.mappers.mappers import BookingsDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingsDataMapper

    




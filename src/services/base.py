

from datetime import date
from src.utils.db_manager import DBManager


class BaseService:
    db: DBManager | None

    def __init__(self, db: DBManager | None = None):
        self.db = db


class DataChecker:
    
    @staticmethod
    async def check_dates(date_from: date, date_to: date) -> None:
        if date_from >= date_to:
            raise DateError

    @staticmethod
    async def check_hotel_available(db: DBManager, hotel_id: int) -> None:
        ...
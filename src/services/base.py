

from datetime import date
from src.exceptions.services import InvalidDatesException
from src.utils.db_manager import DBManager



class BaseService:
    db: DBManager | None

    def __init__(self, db: DBManager | None = None):
        self.db = db

    @staticmethod
    def check_dates(date_from: date, date_to: date) -> None:
        if date_from >= date_to:
            raise InvalidDatesException




from src.database import Base

# Базовые исключения

class UnknownException(Exception):
    detail = 'Неизвестная ошибка'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)



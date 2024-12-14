from sqlalchemy import insert, select
from models.users import UsersOrm
from schemas.users import User
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User
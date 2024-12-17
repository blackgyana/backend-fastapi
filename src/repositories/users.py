from sqlalchemy import select
from src.models.users import UsersOrm
from src.schemas.users import User, UserAdd, UserWithHashedPassword
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, **filter_by) -> UserWithHashedPassword:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)
from sqlalchemy import select
from src.repositories.mappers.mappers import UserWithHashedPasswordDataMapper
from src.models.users import UsersORM
from src.schemas.users import UserWithHashedPasswordDTO
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserWithHashedPasswordDataMapper

    async def get_user_with_hashed_password(self, **filter_by) -> UserWithHashedPasswordDTO:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return self.mapper.to_domain_entity(model)

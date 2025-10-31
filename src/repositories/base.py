from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update, Result
from sqlalchemy.ext.asyncio import AsyncSession

from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import Base
from src.exceptions.base import ObjectAlreadyExistsException, ObjectInBulkNotFoundException, ObjectNotFoundException, UnknownException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model: type[Base]
    mapper: type[DataMapper]

    def __init__(self, session):
        self.session: AsyncSession = session

    def _validate_one(self, result: Result):
        """Валидация ответа на единственную сущность"""
        count = len(result.scalars().all())  # sequence отдает результат только 1 раз
        if count == 0:
            raise ObjectNotFoundException
        elif count > 1:
            raise UnknownException

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        """Получить все сущности"""
        return await self.get_filtered()

    async def get(self, **filter_by) -> BaseModel:
        """Получить 1 сущность"""
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            res = result.scalars().one()
        except NoResultFound as ex:
            raise ObjectNotFoundException from ex
        except Exception as ex:
            raise UnknownException from ex
        return self.mapper.to_domain_entity(res)

    async def get_one_or_none(self, **filter_by):
        """Получить 1 сущность или ничего"""
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        return self.mapper.to_domain_entity(res) if res else None

    async def add(self, data: BaseModel):
        """Добавить сущность"""
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_stmt)
        except (UniqueViolationError, IntegrityError) as ex:
            raise ObjectAlreadyExistsException from ex
        except Exception as ex:
            raise ex
            # raise UnknownException from ex
        return self.mapper.to_domain_entity(result.scalars().one())

    async def add_bulk(self, data: list[BaseModel]):
        """Добавить сущность"""
        add_stmt = (
            insert(self.model).values([obj.model_dump() for obj in data]).returning(self.model)
        )
        try:
            result = await self.session.execute(add_stmt)
        except UniqueViolationError:
            raise ObjectAlreadyExistsException
        except (ForeignKeyViolationError, IntegrityError) as ex:
            raise ObjectInBulkNotFoundException from ex
        except Exception as ex:
            raise UnknownException from ex
        return [self.mapper.to_domain_entity(obj) for obj in result.scalars().all()]

    async def update(self, data: BaseModel, exclude_unset=False, **filter_by):
        """Изменить сущность"""
        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        try:
            result = await self.session.execute(edit_stmt)
            objs = result.scalars().all()
            if len(objs) == 0:
                raise NoResultFound
            data = [self.mapper.to_domain_entity(obj) for obj in objs]
            if len(data) == 1:
                return data[0]
        except NoResultFound as ex:
            raise ObjectNotFoundException from ex

    async def delete(self, *filter, **filter_by) -> None:
        """Удалить сущность"""
        try:
            del_stmt = delete(self.model).filter(*filter).filter_by(**filter_by)
            result = await self.session.execute(del_stmt)
            if result.rowcount == 0:
                raise NoResultFound
        except NoResultFound as ex:
            raise ObjectNotFoundException from ex
        except Exception as ex:
            raise UnknownException from ex

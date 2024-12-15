from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update, Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session: AsyncSession = session

    def _validate_one(self, result: Result):
        '''Валидация ответа на единственную сущность'''
        count = len(result.scalars().all()
                    )  # sequence отдает результат только 1 раз
        if count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        elif count > 1:
            raise HTTPException(status_code=400, detail="Bad request")

    async def get_all(self, *args, **kwargs):
        '''Получить все сущности'''
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        '''Получить 1 сущность или ничего'''
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        return self.schema.model_validate(res) if res else None

    async def add(self, data: BaseModel):
        '''Добавить сущность'''
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        try:
            result = await self.session.execute(add_stmt)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Bad request. Item already exists.")
        return self.schema.model_validate(result.scalars().one())

    async def edit(self, data: BaseModel, exclude_unset=False, **filter_by) -> None:
        '''Изменить сущность'''
        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model.id)
        )
        result = await self.session.execute(edit_stmt)
        self._validate_one(result)

    async def delete(self, **filter_by) -> None:
        '''Удалить сущность'''
        del_stmt = (
            delete(self.model)
            .filter_by(**filter_by)
            .returning(self.model.id)
        )
        result = await self.session.execute(del_stmt)
        self._validate_one(result)

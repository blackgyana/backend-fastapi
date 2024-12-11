from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class BaseRepository:
    model: BaseModel = None

    def __init__(self, session):
        self.session: AsyncSession = session

    def validate_one(self, result):
        count = len(result.scalars().all())
        if count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        elif count > 1:
            raise HTTPException(status_code=400, detail="Bad request")

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(add_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        edit_stmt = (
            update(self.model)
            .values(**data.model_dump())
            .filter_by(**filter_by)
            .returning(self.model.id)
        )
        result = await self.session.execute(edit_stmt)
        self.validate_one(result)

    async def delete(self, **filter_by) -> None:
        del_stmt = (
            delete(self.model)
            .filter_by(**filter_by)
            .returning(self.model.id)
        )
        result = await self.session.execute(del_stmt)
        self.validate_one(result)

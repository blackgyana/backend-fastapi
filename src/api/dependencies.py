from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, gt=0, description='Текущая страница')]
    per_page: Annotated[int | None, Query(3, gt=0, lte=10, description='Количество на странице')]


PaginationDep = Annotated[PaginationParams, Depends()]
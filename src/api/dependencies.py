from typing import Annotated
from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel
import jwt
from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, gt=0, description='Текущая страница')]
    per_page: Annotated[int | None, Query(3, gt=0, lte=10, description='Количество на странице')]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request:Request):
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(401, 'Unauthorized')
    return access_token

def get_current_user_id(token:str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
    except jwt.exceptions.DecodeError:
        raise HTTPException(401, 'Invalid token')   
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(401, 'Token expired')
    return data['uid']

UserIdDep = Annotated[int, Depends(get_current_user_id)]



async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
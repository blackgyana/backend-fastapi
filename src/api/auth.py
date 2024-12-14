from fastapi import APIRouter
from database import async_session_maker
from repositories.users import UsersRepository
from schemas.users import UserAdd, UserRequestAdd
from passlib.context import CryptContext


router = APIRouter(prefix='/auth')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/register')
async def register_user(user_data: UserRequestAdd):
    request_data = user_data.model_dump()
    hashed_password = pwd_context.hash(request_data['password'])
    del request_data['password']
    new_user_data = UserAdd(hashed_password=hashed_password, **request_data)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {'status': 'OK'}
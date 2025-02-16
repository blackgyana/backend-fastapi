from fastapi import APIRouter, HTTPException, Response
from database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import BaseUser, User, UserAdd, UserRequestAdd, UserRequestLogin
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep


router = APIRouter(prefix='/auth')


@router.post('/register')
async def register_user(user_data: UserRequestAdd):
    hashed_password = AuthService().hash_password(user_data.password)
    request_data = user_data.model_dump()
    del request_data['password']
    new_user_data = UserAdd(hashed_password=hashed_password, **request_data)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {'status': 'OK'}


@router.post('/login')
async def login_user(user_data: UserRequestLogin, response: Response):
    async with async_session_maker() as session:
        user: User | None = (
            await UsersRepository(session)
            .get_user_with_hashed_password(email=user_data.email)
        )
        if not user:
            raise HTTPException(
                status_code=401, detail='Пользователь не найден')
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401, detail='Неверные данные входа')
        access_token = AuthService().create_access_token({'uid': user.id})
        response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@router.get('/me')
async def get_me(uid: UserIdDep) -> BaseUser:
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=uid)
    return user


@router.post('/logout') # POST - изменение состояния на сервере
async def logout_user(uid: UserIdDep, response: Response):
    response.delete_cookie('access_token')
    return {'status': 'OK'}
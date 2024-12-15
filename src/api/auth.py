from fastapi import APIRouter, HTTPException, Request, Response
from database import async_session_maker
from repositories.users import UsersRepository
from schemas.users import User, UserAdd, UserRequestAdd, UserRequestLogin
from src.services.auth import AuthService



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
        user: User | None = await UsersRepository(session).get_one_or_none(email=user_data.email)
        if not user: 
            raise HTTPException(status_code=401, detail='Пользователь не найден')
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Неверные данные входа')
        access_token = AuthService().create_access_token({'uid': user.id})
        response.set_cookie('access_token', access_token)
    return {'access_token': access_token}

@router.get('/only_auth')
async def only_auth(request:Request):
    access_token = request.cookies.get('access_token')
    return {'has_access_token': bool(access_token)}
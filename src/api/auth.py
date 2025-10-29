from fastapi import APIRouter, HTTPException, Response
from database import async_session_maker
from src.schemas.users import BaseUser, UserDTO, UserAdd, UserRequestAdd, UserRequestLogin
from src.services.auth import AuthService
from src.api.dependencies import DBDep, UserIdDep
from src.config import settings
from src.exceptions import ObjectAlreadyExistsException, UnknownException

# from src.background_tasks.email import send_email

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register_user(user_data: UserRequestAdd, db: DBDep):
    hashed_password = AuthService().hash_password(user_data.password)
    # убираем пароль
    request_data = user_data.model_dump()
    del request_data["password"]
    new_user_data = UserAdd(hashed_password=hashed_password, **request_data)
    try:
        await db.users.add(new_user_data)
        await db.commit()
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409, detail='Такой пользователь уже существует')
    except Exception as ex:
        raise HTTPException(status_code=409, detail=str(ex))
    except UnknownException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    # Отправка почты в фоне
    # background_tasks.add_task(send_email,
    #         'Регистрация в сервисе',
    #         new_user_data.email,
    #         'Спасибо за регистрация в нашем сервисе!')
    return {"status": "OK"}


@router.post("/login")
async def login_user(user_data: UserRequestLogin, response: Response, db: DBDep):
    async with async_session_maker() as session:
        user: UserDTO | None = await db.users.get_user_with_hashed_password(
            email=user_data.email
        )
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверные данные входа")

        access_token = AuthService().create_access_token({"uid": user.id})
        response.set_cookie(
            "access_token",
            access_token,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            samesite="lax",
            httponly=True,
        )
    return {"access_token": access_token}


@router.get("/me")
async def get_me(uid: UserIdDep, db: DBDep) -> BaseUser:
    async with async_session_maker() as session:
        user = await db.users.get_one_or_none(id=uid)
    return user


@router.post("/logout")  # POST - изменение состояния на сервере
async def logout_user(uid: UserIdDep, response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}

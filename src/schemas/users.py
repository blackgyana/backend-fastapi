from pydantic import BaseModel, EmailStr, ConfigDict


class BaseUser(BaseModel):
    email: EmailStr
    nickname: str | None = None
    first_name: str | None = None
    last_name: str | None = None

class UserRequestAdd(BaseUser):
    password: str

class UserRequestLogin(BaseModel):
    email: EmailStr
    password: str

class UserAdd(BaseUser):
    hashed_password: str



class UserDTO(BaseUser):
    id: int


class UserWithHashedPasswordDTO(UserDTO):
    hashed_password: str
import pydantic
from src.data.schemas.base import BaseSchemaModel


class UserWithToken(BaseSchemaModel):
    token: str
    name: str
    email: pydantic.EmailStr
    is_active: bool
    is_logged_in: bool
    role_id: int


class UserInResponse(BaseSchemaModel):
    id: int
    authorized_account: UserWithToken


class User(BaseSchemaModel):
    id: int
    name: str
    email: pydantic.EmailStr
    role_id: int
    is_active: bool
    is_logged_in: bool

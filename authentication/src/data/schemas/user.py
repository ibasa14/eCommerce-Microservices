import pydantic
from typing import Optional
from src.data.schemas.base import BaseSchemaModel


class UserInCreate(BaseSchemaModel):
    name: str
    email: pydantic.EmailStr
    password: str
    role_id: int


class UserOutCreate(BaseSchemaModel):
    name: str
    email: pydantic.EmailStr
    role_id: int
    is_active: int


class UserInUpdate(BaseSchemaModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None


class UserInLogin(BaseSchemaModel):
    email: str
    password: str


class UserWithToken(BaseSchemaModel):
    token: str
    name: str
    email: pydantic.EmailStr
    is_active: bool
    is_logged_in: bool
    role_id: int


class UserInResponse(BaseSchemaModel):
    id: int
    name: str
    # authorized_account: UserWithToken
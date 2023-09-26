import datetime

import pydantic

from src.data.schemas.base import BaseSchemaModel


class UserInCreate(BaseSchemaModel):
    name: str
    email: pydantic.EmailStr
    password: str


class UserOutCreate(BaseSchemaModel):
    name: str
    email: pydantic.EmailStr
    role_id: int
    is_active: int


class UserInUpdate(BaseSchemaModel):
    name: str | None
    email: str | None
    password: str | None
    is_active: bool | None
    role_id: int | None


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

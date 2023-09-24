import datetime

import pydantic

from src.data.schemas.base import BaseSchemaModel


class UserInCreate(BaseSchemaModel):
    name: str
    email: pydantic.EmailStr
    password: str


class UserInUpdate(BaseSchemaModel):
    name: str | None
    email: str | None
    password: str | None
    is_active: bool | None
    role_id: int | None


class UserInLogin(BaseSchemaModel):
    username: str
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
    authorized_account: UserWithToken

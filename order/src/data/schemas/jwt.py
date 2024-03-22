import datetime

import pydantic


class JWToken(pydantic.BaseModel):
    exp: datetime.datetime
    sub: str


class JWTUser(pydantic.BaseModel):
    name: str
    email: pydantic.EmailStr
    is_active: bool
    is_logged_in: bool
    role_id: int
    scopes: list[str]

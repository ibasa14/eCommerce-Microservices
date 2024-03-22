import datetime

import pydantic
from typing import Optional


class JWToken(pydantic.BaseModel):
    exp: datetime.datetime
    sub: Optional[str] = ""  # Cannot be None


class JWTUser(pydantic.BaseModel):
    name: str
    email: pydantic.EmailStr
    is_active: bool
    is_logged_in: bool
    role_id: int
    scopes: list[str]

import datetime

import pydantic
from jose import jwt as jose_jwt, JWTError as JoseJWTError

from src.config.manager import settings
from src.data.schemas.user import UserOutCreate
from src.data.schemas.jwt import JWTUser, JWToken
from src.utilities.exceptions.database import EntityDoesNotExist


class JWTGenerator:
    def _generate_jwt_token(
        self,
        *,
        jwt_data: dict[str, str],
        expires_delta: datetime.timedelta | None = None,
    ) -> str:
        to_encode = jwt_data.copy()

        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta

        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=settings.JWT_MIN
            )

        to_encode.update(JWToken(exp=expire, sub=settings.JWT_SUBJECT).dict())

        return jose_jwt.encode(
            to_encode,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def generate_access_token(self, user: UserOutCreate) -> str:
        if not user:
            raise EntityDoesNotExist(
                "Cannot generate JWT token for without User entity!"
            )

        return self._generate_jwt_token(
            jwt_data=JWTUser(username=user.name, email=user.email).dict(),  # type: ignore
            expires_delta=datetime.timedelta(
                minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME
            ),
        )

def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()

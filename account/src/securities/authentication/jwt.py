import datetime

from jose import jwt as jose_jwt
from src.config.manager import settings
from src.data.schemas.jwt import JWToken, JWTUser
from src.data.schemas.user import User
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
            expire = (
                datetime.datetime.now(datetime.timezone.utc) + expires_delta
            )

        else:
            expire = datetime.datetime.now(
                datetime.timezone.utc
            ) + datetime.timedelta(minutes=settings.JWT_MIN)

        to_encode.update(JWToken(exp=expire).model_dump())

        return jose_jwt.encode(
            to_encode,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def generate_access_token(self, user: User) -> str:
        if not user:
            raise EntityDoesNotExist(
                "Cannot generate JWT token for without User entity!"
            )
        scopes = [
            "product:read",
            "product:update",
            "order:read",
            "order:create",
        ]
        if user.role_id == 1:
            scopes += [
                "product:create",
                "product:delete",
                "order:read-all",
                "order:delete",
            ]

        data = user.model_dump() | dict(scopes=scopes)
        return self._generate_jwt_token(
            jwt_data=JWTUser(**data).model_dump(),  # type: ignore
            expires_delta=datetime.timedelta(
                minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME
            ),
        )


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()

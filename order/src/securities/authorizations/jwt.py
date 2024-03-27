import datetime

import pydantic
from jose import jwt as jose_jwt, JWTError as JoseJWTError

from src.config.manager import settings
from src.data.schemas.user import UserInResponse
from src.data.schemas.jwt import JWTUser


class JWTRetriever:
    @property
    def secret_key(self):
        return settings.JWT_SECRET_KEY

    @property
    def algorithm(self):
        return settings.JWT_ALGORITHM

    def retrieve_user_details_from_token(
        self, token: UserInResponse
    ) -> JWTUser:
        try:
            payload = jose_jwt.decode(
                token=token, key=self.secret_key, algorithms=[self.algorithm]
            )
            attrs = payload | {"token":token}
            jwt_user = JWTUser(**attrs)

        except JoseJWTError as token_decode_error:
            raise ValueError(
                "Unable to decode JWT Token"
            ) from token_decode_error

        except pydantic.ValidationError as validation_error:
            raise ValueError("Invalid payload in token") from validation_error

        return jwt_user


def get_jwt_retriever() -> JWTRetriever:
    return JWTRetriever()


jwt_retriever: JWTRetriever = get_jwt_retriever()

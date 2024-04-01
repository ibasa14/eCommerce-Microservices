from typing import Annotated

import fastapi
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError
from src.config.manager import settings
from src.data.schemas.jwt import JWTUser
from src.securities.authorizations.jwt import jwt_retriever
from src.utilities.exceptions.http.exc_403 import (
    http_403_exc_not_active_account,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.AUTHENTICATION_URL)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, fastapi.Depends(oauth2_scheme)],
) -> JWTUser:
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        jwt_user = jwt_retriever.retrieve_user_details_from_token(token)
    except JWTError:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in jwt_user.scopes:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={
                    "WWW-Authenticate": (
                        f"Bearer scope={security_scopes.scope_str}"
                    )
                },
            )
    return jwt_user


async def get_current_active_user(
    current_user: Annotated[JWTUser, fastapi.Depends(get_current_user)]
) -> JWTUser:
    if not current_user.is_active:
        raise http_403_exc_not_active_account(email=current_user.email)
    return current_user

import fastapi
from typing import Annotated
from src.api.dependencies.repository import get_repository
import src.data.schemas.user as UserSchema
from src.data.models import User
from src.crud.user import UserCRUD
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from src.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)
from src.securities.authentication.jwt import jwt_generator
from src.config.manager import settings

router = fastapi.APIRouter(
    prefix=settings.AUTHENTICATION_ROUTER, tags=["authentication"]
)


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_crud: UserCRUD = fastapi.Depends(
        get_repository(repo_type=UserCRUD, model=User)
    ),
):
    try:
        db_user = await user_crud.read_user_by_password_authentication(
            user_login=form_data
        )

    except Exception:
        raise await http_exc_400_credentials_bad_signin_request()

    access_token = jwt_generator.generate_access_token(
        user=UserSchema.User(**db_user.to_dict())
    )

    return UserSchema.UserInResponse(
        id=db_user.id,
        authorized_account=UserSchema.UserWithToken(
            token=access_token,
            name=db_user.name,
            email=db_user.email,  # type: ignore
            is_active=db_user.is_active,
            is_logged_in=db_user.is_logged_in,
            role_id=db_user.role_id,
        ),
    )

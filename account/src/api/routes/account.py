import fastapi
import pydantic
import src.data.schemas.user as UserSchema
from src.api.dependencies.repository import get_repository
from src.constants import ACCOUNT_ROUTER_URL
from src.crud.user import UserCRUD
from src.data.models import User
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_400 import http_400_exc_bad_email_request

router = fastapi.APIRouter(prefix=ACCOUNT_ROUTER_URL, tags=["account"])


@router.get(
    path="/{email}",
    name="account:get-user-by-email",
    response_model=UserSchema.User,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_user_by_email(
    email: pydantic.EmailStr,
    user_crud: UserCRUD = fastapi.Depends(
        get_repository(repo_type=UserCRUD, model=User)
    ),
) -> UserSchema.User:
    try:
        user_db = await user_crud.read_user_by_email(email=email)

    except EntityDoesNotExist:
        raise await http_400_exc_bad_email_request(email=email)

    return UserSchema.User(**user_db.to_dict())

import fastapi
import pydantic
from typing import List, Dict
from src.api.dependencies.repository import get_repository
import src.data.schemas.user as UserSchema
from src.data.models import User
from src.crud.user import UserCRUD
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_email_not_found_request,
    http_404_exc_id_not_found_request,
    http_404_exc_username_not_found_request,
)

router = fastapi.APIRouter(prefix="/user", tags=["user"])


@router.get(
    path="",
    name="users:get-multiple-user",
    response_model=List[UserSchema.UserInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_multiple_user(
    user_crud: UserCRUD = fastapi.Depends(
        get_repository(repo_type=UserCRUD, model=User)
    ),
) -> List[UserSchema.UserInResponse]:
    db_users = await user_crud.get_multiple()
    db_users_list: list = list()

    for db_user in db_users:
        user = UserSchema.UserInResponse(id=db_user.id, name=db_user.name)
        db_users_list.append(user)

    return db_users_list


@router.get(
    path="/{id}",
    name="users:get-user",
    response_model=UserSchema.UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_user(
    id: int,
    user_crud: UserCRUD = fastapi.Depends(
        get_repository(repo_type=UserCRUD, model=User)
    ),
) -> UserSchema.UserInResponse:
    try:
        db_user = await user_crud.get(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return UserSchema.UserInResponse(id=db_user.id, name=db_user.name)


@router.post(
    path="/",
    name="user:post-user",
    response_model=UserSchema.UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def create_user(
    user_create: UserSchema.UserInResponse,
    user_crud: UserCRUD = fastapi.Depends(
        get_repository(repo_type=UserCRUD, model=User)
    ),
) -> UserSchema.UserInResponse:
    created_user = await user_crud.create_user(user_create=user_create)

    return UserSchema.UserInResponse(id=created_user.id, name=created_user.name)


@router.put(
    path="/{id}",
    name="user:update-user",
    response_model=UserSchema.UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_user(
    query_id: int,
    user_in_update: UserSchema.UserInUpdate,
    user_crud: UserCRUD = fastapi.Depends(
        get_repository(repo_type=UserCRUD, model=User)
    ),
) -> UserSchema.UserInResponse:
    user_update = UserSchema.UserInUpdate(user_in_update)
    try:
        updated_db_user = await user_crud.update_user(
            id=query_id, user_update=user_update
        )

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=query_id)

    return UserSchema.UserInResponse(
        id=updated_db_user.id, name=updated_db_user.name
    )


@router.delete(
    path="",
    name="user:delete-user",
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_account(
    id: int,
    user_crud: UserCRUD = fastapi.Depends(
        get_repository(repo_type=UserCRUD, model=User)
    ),
) -> Dict[str, str]:
    try:
        deletion_result = await user_crud.delete(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return {"notification": deletion_result}

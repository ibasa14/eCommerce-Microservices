import typing
from typing import TypeVar

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from src.api.dependencies.session import get_async_session
from src.crud.base import BaseCRUD
from src.data.database import SqlAlchemyBase

ModelType = TypeVar("ModelType", bound=SqlAlchemyBase)


def get_repository(
    repo_type: typing.Type[BaseCRUD], model: type[ModelType]
) -> typing.Callable[[SQLAlchemyAsyncSession], BaseCRUD]:
    def _get_repo(
        async_session: SQLAlchemyAsyncSession = fastapi.Depends(
            get_async_session
        ),
    ) -> BaseCRUD:
        return repo_type(async_session=async_session, model=model)

    return _get_repo

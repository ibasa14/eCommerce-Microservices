import typing

import fastapi
from sqlalchemy.ext.asyncio import (
    AsyncSession as SQLAlchemyAsyncSession,
)

from src.api.dependencies.session import get_async_session
from src.crud.base import BaseCRUD


def get_repository(
    repo_type: typing.Type[BaseCRUD],
) -> typing.Callable[[SQLAlchemyAsyncSession], BaseCRUD]:
    def _get_repo(
        async_session: SQLAlchemyAsyncSession = fastapi.Depends(
            get_async_session
        ),
    ) -> BaseCRUD:
        return repo_type(async_session=async_session)

    return _get_repo

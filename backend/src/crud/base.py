from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from typing import TypeVar, Type, Any, Optional, Sequence
from src.data.database import SqlAlchemyBase
import sqlalchemy
from src.utilities.exceptions.database import (
    EntityDoesNotExist,
)

ModelType = TypeVar("ModelType", bound=SqlAlchemyBase)


class BaseCRUD:
    def __init__(
        self, async_session: SQLAlchemyAsyncSession, model: Type[ModelType]
    ):
        self.async_session = async_session
        self.model = model

    async def get(self, id: Any) -> Optional[ModelType]:
        stmt = sqlalchemy.select(self.model).where(self.model.id == id)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(
                f"{self.__class__.__name__} with id: {id} does not exist"
            )
        return query.scalar()

    async def get_multiple(self) -> Optional[Sequence[ModelType]]:
        stmt = sqlalchemy.select(self.model)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def delete(self, id: int) -> str:
        select_stmt = sqlalchemy.select(self.model).where(self.model.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_instance = query.scalar()

        if not delete_instance:
            raise EntityDoesNotExist(f"{self.model.__class__.__name__} with id `{id}` does not exist!")  # type: ignore

        stmt = sqlalchemy.delete(table=self.model).where(
            self.model.id == delete_instance.id
        )

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"{self.model.__class__.__name__} with id '{id}' is successfully deleted!"

    async def delete_multiple(self) -> str:
        stmt = sqlalchemy.delete(table=self.model)
        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"{self.model.__class__.__name__} table cleaned!"

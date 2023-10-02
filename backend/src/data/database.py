import pydantic
from sqlalchemy.ext.asyncio import (
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    create_async_engine as create_sqlalchemy_async_engine,
)
from sqlalchemy.pool import (
    Pool as SQLAlchemyPool,
    QueuePool as SQLAlchemyQueuePool,
)
from sqlalchemy.orm import declarative_base
from src.config.manager import settings


class AsyncDatabase:
    def __init__(self, db_name=settings.DB_POSTGRES_NAME):
        self.postgres_uri: str = f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/{db_name}"

        self.async_engine: SQLAlchemyAsyncEngine = (
            create_sqlalchemy_async_engine(
                url=self.set_async_db_uri,
                echo=settings.IS_DB_ECHO_LOG,
                pool_size=settings.DB_POOL_SIZE,
                max_overflow=settings.DB_POOL_OVERFLOW,
                poolclass=SQLAlchemyQueuePool,
            )
        )
        self.async_session: SQLAlchemyAsyncSession = SQLAlchemyAsyncSession(
            bind=self.async_engine
        )
        self.pool: SQLAlchemyPool = self.async_engine.pool

    @property
    def set_async_db_uri(self) -> str | pydantic.PostgresDsn:
        """
        Set the synchronous database driver into asynchronous version by utilizing AsyncPG:

            `postgresql://` => `postgresql+asyncpg://`
        """
        return (
            self.postgres_uri.replace("postgresql://", "postgresql+asyncpg://")
            if self.postgres_uri
            else self.postgres_uri
        )


async_db: AsyncDatabase = AsyncDatabase()

SqlAlchemyBase = declarative_base()

from .models import Product, Role, User

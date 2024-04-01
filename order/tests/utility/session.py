import typing

from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from src.data.database import AsyncDatabase

async_db_testing: AsyncDatabase = AsyncDatabase(
    db_name="postgres_order_testing"
)


async def get_async_session_testing() -> (
    typing.AsyncGenerator[SQLAlchemyAsyncSession, None]
):
    try:
        yield async_db_testing.async_session
    except Exception:
        await async_db_testing.async_session.rollback()
    finally:
        await async_db_testing.async_session.close()

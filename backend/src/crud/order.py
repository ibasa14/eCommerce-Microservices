import sqlalchemy

from src.data.models import Order
from src.data.schemas.order import (
    OrderInCreate,
    OrderInUpdate,
    OrderInResponse,
)
from src.crud.base import BaseCRUD

from src.utilities.exceptions.database import (
    EntityAlreadyExists,
    EntityDoesNotExist,
)


class OrderCRUD(BaseCRUD):
    async def create_order(
        self, order_create: OrderInCreate
    ) -> OrderInResponse:
        new_order = Order(**order_create.dict(exclude_none=True))
        self.async_session.add(instance=new_order)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_order)
        return new_order

    async def update_order(self, id: int, order_update: OrderInUpdate) -> Order:
        new_order_data = order_update.dict(exclude_none=True)

        select_stmt = sqlalchemy.select(Order).where(Order.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_order = query.scalar()

        if not update_order:
            raise EntityDoesNotExist(f"Order with id `{id}` does not exist!")  # type: ignore

        update_stmt = sqlalchemy.update(table=Order).where(Order.id == update_order.id)  # type: ignore

        for key in new_order_data:
            update_stmt = update_stmt.values({key: new_order_data[key]})

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_order)

        return update_order  # type: ignore

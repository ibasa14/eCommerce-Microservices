import sqlalchemy

from src.data.models import Order
from src.data.schemas.order import (
    OrderInCreate,
    OrderInUpdate,
    OrderInResponse,
)
from src.crud.base import BaseCRUD

from src.utilities.exceptions.database import (
    EntityDoesNotExist,
)

from typing import Optional, Sequence


class OrderCRUD(BaseCRUD):
    async def get_multiple(
        self,
        categories: str | None,
        order_by: str | None,
        order_type: str,
        min_cost: float | None,
        max_cost: float | None,
    ) -> Optional[Sequence[Order]]:
        stmt = sqlalchemy.select(Order)
        if categories:
            categories_list = [int(cat) for cat in categories.split(",")]
            stmt = stmt.filter(Order.category_id.in_(categories_list))
        if min_cost:
            stmt = stmt.filter(Order.price >= min_cost)
        if max_cost:
            stmt = stmt.filter(Order.price <= max_cost)
        if order_by:
            stmt = stmt.order_by(
                getattr(getattr(Order, order_by), order_type)()
            )

        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def create_order(
        self, order_create: OrderInCreate
    ) -> OrderInResponse:
        new_order = Order(**order_create.model_dump(exclude_none=True))
        self.async_session.add(instance=new_order)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_order)
        return new_order

    async def read_order_by_ordername(self, ordername: str) -> Order:
        stmt = sqlalchemy.select(Order).where(Order.name == ordername)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(
                "Order with ordername `{ordername}` does not exist!"
            )

        return query.scalar()  # type: ignore

    async def update_order(self, id: int, order_update: OrderInUpdate) -> Order:
        new_order_data = order_update.model_dump(exclude_none=True)

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

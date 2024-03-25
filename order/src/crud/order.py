import sqlalchemy
from sqlalchemy.orm import joinedload, selectinload
from src.data.models import Order, OrderDetail
from src.crud.base import BaseCRUD
from src.data.schemas.order import OrderWithDetails
from src.data.schemas.order_detail import OrderDetailForSpecificOrder
from src.utilities.exceptions.database import (
    EntityDoesNotExist,
)

from typing import Optional, Sequence, List


class OrderCRUD(BaseCRUD):
    ORDER_BY_TRANSLATOR = {"price": "total_price", "date": "date"}

    async def get(self, id: int) -> Optional[OrderWithDetails]:
        # create a select statement to get the order with the given id with all the OrderDetails
        stmt = sqlalchemy.select(Order).where(Order.id == id)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(
                f"{self.__class__.__name__} with id: {id} does not exist"
            )
        return query.scalar()

    async def get_multiple(
        self,
        users_id: List[int] | None,
        order_by: str | None,
        order_type: str,
        min_cost: float | None,
        max_cost: float | None,
    ) -> Optional[Sequence[Order]]:
        stmt = sqlalchemy.select(Order)
        if users_id:
            stmt = stmt.filter(Order.user_id.in_(users_id))
        if min_cost:
            stmt = stmt.filter(Order.total_price >= min_cost)
        if max_cost:
            stmt = stmt.filter(Order.total_price <= max_cost)
        if order_by:
            stmt = stmt.order_by(
                getattr(
                    getattr(Order, self.ORDER_BY_TRANSLATOR.get(order_by)),
                    order_type,
                )()
            )

        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def create_order(
        self, order_create: List[OrderDetailForSpecificOrder], user_id: int
    ) -> Order:
        total_price = sum([order.total for order in order_create])
        order = Order(total_price=total_price, user_id=user_id)
        self.async_session.add(order)
        await self.async_session.flush()
        for order_detail in order_create:
            order_detail = OrderDetail(
                **order_detail.model_dump(), order_id=order.id
            )
            self.async_session.add(order_detail)
        await self.async_session.commit()
        await self.async_session.refresh(instance=order)
        return order

import sqlalchemy

from src.data.models import OrderDetail, Order, Product
from src.data.schemas.order_detail import (
    OrderDetailInput,
    OrderDetailInUpdate,
    OrderDetailInResponse,
)

from src.crud.base import BaseCRUD

from src.utilities.exceptions.database import (
    EntityAlreadyExists,
    EntityDoesNotExist,
)
from typing import List


class OrderDetailCRUD(BaseCRUD):
    async def create_order_detail(
        self, order_detail_create_list: List[OrderDetailInput]
    ) -> List[OrderDetailInResponse]:
        # NOTE: hardcoded user_id, this will be updated once we use authentication
        new_order = Order(user_id=2)
        self.async_session.add(instance=new_order)
        await self.async_session.flush()
        order_detail_in_response = []
        for order_detail in order_detail_create_list:
            order_detail_sql:OrderDetail = OrderDetail(**order_detail.model_dump())
            product_sql:Product = await self.async_session.get(entity=Product, ident=order_detail_sql.product_id)
            order_detail_sql.order_id = new_order.id
            order_detail_sql.total=product_sql.price*order_detail_sql.quantity
            product_sql.stock-=order_detail_sql.quantity
            new_order.total+=order_detail_sql.total
            self.async_session.add(order_detail_sql)
            self.async_session.add(product_sql)
            await self.async_session.flush()
            order_detail_in_response.append(OrderDetailInResponse(**order_detail_sql.to_dict()))
        await self.async_session.commit()
        return order_detail_in_response

    async def update_order_detail(
        self, id: int, order_detail_update: OrderDetailInUpdate
    ) -> OrderDetail:
        new_order_detail_data = order_detail_update.dict(exclude_none=True)

        select_stmt = sqlalchemy.select(OrderDetail).where(OrderDetail.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_order_detail = query.scalar()

        if not update_order_detail:
            raise EntityDoesNotExist(f"OrderDetail with id `{id}` does not exist!")  # type: ignore

        update_stmt = sqlalchemy.update(table=OrderDetail).where(OrderDetail.id == update_order_detail.id)  # type: ignore

        for key in new_order_detail_data:
            update_stmt = update_stmt.values({key: new_order_detail_data[key]})

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_order_detail)

        return update_order_detail  # type: ignore

from typing import List
import datetime
from src.data.schemas.base import BaseSchemaModel
from src.data.schemas.order_detail import (
    OrderDetail,
    OrderDetailForSpecificOrder,
)


class Order(BaseSchemaModel):
    date: datetime.datetime
    total_price: float


class OrderDB(Order):
    id: int
    user_id: int


class OrderWithDetails(Order):
    details: list[OrderDetail]

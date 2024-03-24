from typing import Optional
import datetime
from src.data.schemas.base import BaseSchemaModel
from src.data.schemas.order_detail import OrderDetail


class Order(BaseSchemaModel):
    date: datetime.datetime
    total_price: float


class OrderDB(Order):
    id: int
    user_id: int


class OrderInCreate(BaseSchemaModel):
    user_id: int
    total_price: float


class OrderWithDetails(Order):
    details: list[OrderDetail]

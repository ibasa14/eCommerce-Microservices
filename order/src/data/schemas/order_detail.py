from typing import Optional
import datetime
from src.data.schemas.base import BaseSchemaModel


class OrderDetail(BaseSchemaModel):
    quantity: int
    total: float
    order_id: int
    product_id: int


class OrderDetailDB(OrderDetail):
    id: int

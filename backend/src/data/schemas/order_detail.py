from typing import Optional
from src.data.schemas.base import BaseSchemaModel


class OrderDetailInput(BaseSchemaModel):
    product_id: int
    quantity: int

class OrderDetailInUpdate(BaseSchemaModel):
    product_id: Optional[int] = None
    order_id: Optional[int] = None
    quantity: Optional[int] = None
    total: Optional[float] = None


class OrderDetailInResponse(OrderDetailInput):
    id: int
    total: float
    order_id: int

from src.data.schemas.base import BaseSchemaModel


class OrderDetailForSpecificOrder(BaseSchemaModel):
    quantity: int
    total: float
    product_id: int


class OrderDetail(OrderDetailForSpecificOrder):
    order_id: int


class OrderDetailDB(OrderDetail):
    id: int

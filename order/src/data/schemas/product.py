from src.data.schemas.base import BaseSchemaModel


class ProductToSubstract(BaseSchemaModel):
    id: int
    quantity: int

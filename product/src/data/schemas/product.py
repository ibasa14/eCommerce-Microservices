from typing import Optional

from src.data.schemas.base import BaseSchemaModel


class ProductInCreate(BaseSchemaModel):
    name: str
    description: str
    picture: Optional[str] = None
    price: float
    stock: int
    category_id: int


class ProductInUpdate(BaseSchemaModel):
    name: Optional[str] = None
    description: Optional[str] = None
    picture: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None


class ProductInResponse(BaseSchemaModel):
    id: int
    name: str
    description: str
    picture: str
    price: float
    stock: int
    category_id: int


class ProductToSubstract(BaseSchemaModel):
    id: int
    quantity: int

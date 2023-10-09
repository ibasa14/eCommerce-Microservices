from typing import Optional
from src.data.schemas.base import BaseSchemaModel
from datetime import datetime


class OrderInCreate(BaseSchemaModel):
    user_id: int


class OrderInUpdate(BaseSchemaModel):
    total: Optional[float] = 0


class OrderInResponse(BaseSchemaModel):
    id: int
    user_id: int
    date: datetime
    total: float

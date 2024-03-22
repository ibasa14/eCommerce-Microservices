import enum

from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import SqlAlchemyBase  # type: ignore


class Order(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "orders"

    id: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    user_id: Column[String] = Column(String, nullable=False)  # type: ignore
    date: Column[DateTime] = Column(DateTime, server_default=func.now())  # type: ignore
    total_price: Column[Float] = Column(Float, nullable=False)  # type: ignore

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date,
            "total_price": self.total_price,
        }


class OrderDetail(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "order_details"

    id: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    quantity: Column[Integer] = Column(Integer, nullable=False)  # type: ignore
    total: Column[Float] = Column(Float, nullable=False)  # type: ignore
    order_id: Column[Integer] = Column(Integer, ForeignKey("orders.id"))  # type: ignore
    product_id: Column[Integer] = Column(Integer, nullable=False)  # type: ignore
    order = relationship("Order", back_populates="order_details", uselist=True, cascade="all, delete")  # type: ignore

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total": self.total,
        }

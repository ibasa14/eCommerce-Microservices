import enum
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    func,
    Integer,
    String,
)
from sqlalchemy.orm import relationship, Relationship

from .database import SqlAlchemyBase  # type: ignore


class RoleType(enum.Enum):
    admin: str = "admin"
    client: str = "client"


class CategoryType(enum.Enum):
    meat: str = "meat"
    seafood: str = "seafood"
    beverage: str = "beverage"
    nonfood: str = "nonfood"
    bakery: str = "bakery"


class User(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "users"

    id_user: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Column[String] = Column(String, nullable=False, unique=True)
    email: Column[String] = Column(String, nullable=False, unique=True)
    hashed_password: Column[String] = Column(String, nullable=False)
    is_active: Column[Boolean] = Column(Boolean, default=True)
    role_id: Column[Integer] = Column(Integer, ForeignKey("roles.id_role"))
    role: Relationship[Any] = relationship("Role")
    orders: Relationship[Any] = relationship("Order", back_populates="user")


class Role(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "roles"
    id_role: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Column[Enum] = Column(Enum(RoleType))


class Product(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "products"

    id_product: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Column[String] = Column(String, nullable=False)
    description: Column[String] = Column(String)
    picture: Column[String] = Column(String, default="not_defined.png")
    price: Column[Float] = Column(Float, nullable=False)
    stock: Column[Integer] = Column(Integer, default=0)
    category_id: Column[Enum] = Column(Enum(CategoryType))
    category: Relationship[Any] = relationship(
        "Category", back_populates="products"
    )


class Category(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "categories"
    id_category: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Column[Enum] = Column(Enum(CategoryType))
    products: Relationship[Any] = relationship(
        "Product", back_populates="category"
    )


class Order(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "orders"

    id_order: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Column[Integer] = Column(Integer, ForeignKey("users.id_user"))
    user: Relationship[Any] = relationship("User", back_populates="orders")
    date: Column[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    total: Column[Float] = Column(Float, default=0)
    order_detail: Relationship[Any] = relationship(
        "OrderDetail", back_populates="order"
    )


class OrderDetail(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "order_details"

    id_order_detail: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    product_id: Column[Integer] = Column(
        Integer, ForeignKey("products.id_product")
    )
    product: Relationship[Any] = relationship(
        "Product", back_populates="order_detail"
    )
    order_id: Column[Integer] = Column(Integer, ForeignKey("orders.id_order"))
    order: Relationship[Any] = relationship(
        "Order", back_populates="order_details"
    )
    quantity: Column[Integer] = Column(Integer, nullable=False)
    total: Column[Float] = Column(Float, default=0)
    __table_args__: CheckConstraint = (
        CheckConstraint(quantity > 0, name="check_quantity_positive"),
    )

import enum
from typing import Any, Tuple

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
    )  # type: ignore
    name: Column[String] = Column(String, nullable=False, unique=True)  # type: ignore
    email: Column[String] = Column(String, nullable=False, unique=True)  # type: ignore
    hashed_password: Column[String] = Column(String, nullable=False)  # type: ignore
    hash_salt: Column[String] = Column(String, nullable=False)  # type: ignore
    is_active: Column[Boolean] = Column(Boolean, default=True)  # type: ignore
    is_logged_in: Column[Boolean] = Column(Boolean, default=False)  # type: ignore
    role_id: Column[Integer] = Column(Integer, ForeignKey("roles.id_role"))  # type: ignore
    role: Relationship[Any] = relationship("Role")  # type: ignore
    orders: Relationship[Any] = relationship("Order", back_populates="user")  # type: ignore


class Role(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "roles"
    id_role: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    name: Column[Enum] = Column(Enum(RoleType))  # type: ignore


class Product(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "products"

    id_product: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    name: Column[String] = Column(String, nullable=False)  # type: ignore
    description: Column[String] = Column(String)  # type: ignore
    picture: Column[String] = Column(String, default="not_defined.png")  # type: ignore
    price: Column[Float] = Column(Float, nullable=False)  # type: ignore
    stock: Column[Integer] = Column(Integer, default=0)  # type: ignore
    category_id: Column[Enum] = Column(Enum(CategoryType))  # type: ignore
    category: Relationship[Any] = relationship(
        "Category", back_populates="products"
    )  # type: ignore


class Category(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "categories"
    id_category: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    name: Column[Enum] = Column(Enum(CategoryType))
    products: Relationship[Any] = relationship(
        "Product", back_populates="category"
    )  # type: ignore


class Order(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "orders"

    id_order: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    user_id: Column[Integer] = Column(Integer, ForeignKey("users.id_user"))  # type: ignore
    user: Relationship[Any] = relationship("User", back_populates="orders")  # type: ignore
    date: Column[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )  # type: ignore
    total: Column[Float] = Column(Float, default=0)  # type: ignore
    order_detail: Relationship[Any] = relationship(
        "OrderDetail", back_populates="order"
    )  # type: ignore


class OrderDetail(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "order_details"

    id_order_detail: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    product_id: Column[Integer] = Column(
        Integer, ForeignKey("products.id_product")
    )  # type: ignore
    product: Relationship[Any] = relationship(
        "Product", back_populates="order_detail"
    )  # type: ignore
    order_id: Column[Integer] = Column(Integer, ForeignKey("orders.id_order"))  # type: ignore
    order: Relationship[Any] = relationship(
        "Order", back_populates="order_details"
    )  # type: ignore
    quantity: Column[Integer] = Column(Integer, nullable=False)  # type: ignore
    total: Column[Float] = Column(Float, default=0)  # type: ignore
    __table_args__: Tuple[CheckConstraint] = (
        CheckConstraint(quantity > 0, name="check_quantity_positive"),
    )  # type: ignore

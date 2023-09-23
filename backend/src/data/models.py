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
from sqlalchemy.types import TypeEngine
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

    id_user: TypeEngine[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name: TypeEngine[String] = Column(String, nullable=False, unique=True)
    email: TypeEngine[String] = Column(String, nullable=False, unique=True)
    hashed_password: TypeEngine[String] = Column(String, nullable=False)
    is_active: TypeEngine[Boolean] = Column(Boolean, default=True)
    role_id: TypeEngine[Integer] = Column(Integer, ForeignKey("roles.id_role"))
    role: Relationship[Any] = relationship("Role")
    orders: Relationship[Any] = relationship("Order", back_populates="user")


class Role(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "roles"
    id_role: TypeEngine[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name: TypeEngine[Enum] = Column(Enum(RoleType))


class Product(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "products"

    id_product: TypeEngine[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name: TypeEngine[String] = Column(String, nullable=False)
    description: TypeEngine[String] = Column(String)
    picture: TypeEngine[String] = Column(String, default="not_defined.png")
    price: TypeEngine[Float[Any]] = Column(Float, nullable=False)
    stock: TypeEngine[Integer] = Column(Integer, default=0)
    category_id: TypeEngine[Enum] = Column(Enum(CategoryType))
    category: Relationship[Any] = relationship(
        "Category", back_populates="products"
    )


class Category(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "categories"
    id_category: TypeEngine[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name: TypeEngine[Enum] = Column(Enum(CategoryType))
    products: Relationship[Any] = relationship(
        "Product", back_populates="category"
    )


class Order(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "orders"

    id_order: TypeEngine[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: TypeEngine[Integer] = Column(Integer, ForeignKey("users.id_user"))
    user: Relationship[Any] = relationship("User", back_populates="orders")
    date: TypeEngine[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    total: TypeEngine[Float] = Column(Float, default=0)
    order_detail: Relationship[Any] = relationship(
        "OrderDetail", back_populates="order"
    )


class OrderDetail(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "order_details"

    id_order_detail: TypeEngine[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    product_id: TypeEngine[Integer] = Column(
        Integer, ForeignKey("products.id_product")
    )
    product: Relationship[Any] = relationship(
        "Product", back_populates="order_detail"
    )
    order_id: TypeEngine[Integer] = Column(
        Integer, ForeignKey("orders.id_order")
    )
    order: Relationship[Any] = relationship(
        "Order", back_populates="order_details"
    )
    quantity: TypeEngine[Integer] = Column(Integer, nullable=False)
    total: TypeEngine[Float[Any]] = Column(Float, default=0)
    __table_args__: Tuple[CheckConstraint] = (
        CheckConstraint(quantity > 0, name="check_quantity_positive"),
    )

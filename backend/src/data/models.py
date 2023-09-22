import enum

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
from sqlalchemy.orm import relationship

from .database import SqlAlchemyBase  # type: ignore


class RoleType(enum.Enum):
    admin = "admin"
    client = "client"


class CategoryType(enum.Enum):
    meat = "meat"
    seafood = "seafood"
    beverage = "beverage"
    nonfood = "nonfood"
    bakery = "bakery"


class User(SqlAlchemyBase):  # type: ignore
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id_role"))
    role = relationship("Role")
    orders = relationship("Order", back_populates="user")


class Role(SqlAlchemyBase):  # type: ignore
    __tablename__ = "roles"
    id_role = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(RoleType))


class Product(SqlAlchemyBase):  # type: ignore
    __tablename__ = "products"

    id_product = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    picture = Column(String, default="not_defined.png")
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Enum(CategoryType))
    category = relationship("Category", back_populates="products")


class Category(SqlAlchemyBase):  # type: ignore
    __tablename__ = "categories"
    id_category = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(CategoryType))
    products = relationship("Product", back_populates="category")


class Order(SqlAlchemyBase):  # type: ignore
    __tablename__ = "orders"

    id_order = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id_user"))
    user = relationship("User", back_populates="orders")
    date = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Float, default=0)
    order_detail = relationship("OrderDetail", back_populates="order")


class OrderDetail(SqlAlchemyBase):  # type: ignore
    __tablename__ = "order_details"

    id_order_detail = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id_product"))
    product = relationship("Product", back_populates="order_detail")
    order_id = Column(Integer, ForeignKey("orders.id_order"))
    order = relationship("Order", back_populates="order_details")
    quantity = Column(Integer, nullable=False)
    total = Column(Float, default=0)
    __table_args__ = (
        CheckConstraint(quantity > 0, name="check_quantity_positive"),
    )

import enum

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    CheckConstraint,
)
from sqlalchemy.orm import relationship

from .database import SqlAlchemyBase  # type: ignore


class CategoryType(enum.Enum):
    meat: str = "meat"
    seafood: str = "seafood"
    beverage: str = "beverage"
    nonfood: str = "nonfood"
    bakery: str = "bakery"


class Product(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "products"

    id: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    name: Column[String] = Column(String, nullable=False)  # type: ignore
    description: Column[String] = Column(String)  # type: ignore
    picture: Column[String] = Column(String, server_default="not_defined.png", nullable=False)  # type: ignore
    price: Column[Float] = Column(Float, CheckConstraint("price>=0"), nullable=False)  # type: ignore
    stock: Column[Integer] = Column(Integer, CheckConstraint("stock>=0"), default=0)  # type: ignore
    category_id: Column[Integer] = Column(Integer, ForeignKey("categories.id"))  # type: ignore
    category = relationship(
        "Category", back_populates="products"
    )  # type: ignore

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "picture": self.picture,
            "price": self.price,
            "stock": self.stock,
            "category_id": self.category_id,
        }


class Category(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "categories"
    id: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    name: Column[String] = Column(String, nullable=False)
    products = relationship(
        "Product",
        back_populates="category",
        uselist=False,
        cascade="all, delete",
    )  # type: ignore

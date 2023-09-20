from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import SqlAlchemyBase  # type: ignore


class User(SqlAlchemyBase):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Product(SqlAlchemyBase):  # type: ignore
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    picture = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)


class Role(SqlAlchemyBase):  # type: ignore
    __tablename__ = "roles"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

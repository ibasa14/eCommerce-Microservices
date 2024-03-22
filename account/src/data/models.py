from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .database import SqlAlchemyBase  # type: ignore


class User(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "users"

    id: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    name: Column[String] = Column(String, nullable=False, unique=True)  # type: ignore
    email: Column[String] = Column(String, nullable=False, unique=True)  # type: ignore
    hashed_password: Column[String] = Column(String, nullable=False)  # type: ignore
    is_active: Column[Boolean] = Column(Boolean, default=True)  # type: ignore
    is_logged_in: Column[Boolean] = Column(Boolean, default=False)  # type: ignore
    role_id: Column[Integer] = Column(Integer, ForeignKey("roles.id"))  # type: ignore
    role = relationship("Role", back_populates="users")  # type: ignore

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active,
            "is_logged_in": self.is_logged_in,
            "role_id": self.role_id,
        }

class Role(SqlAlchemyBase):  # type: ignore
    __tablename__: str = "roles"

    id: Column[Integer] = Column(
        Integer, primary_key=True, autoincrement=True
    )  # type: ignore
    name: Column[String] = Column(String, nullable=False)  # type: ignore
    users = relationship("User", back_populates="role", uselist=False, cascade="all, delete")  # type: ignore

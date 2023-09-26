import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.data.models import User
from src.data.schemas.user import (
    UserInCreate,
    UserOutCreate,
    UserInLogin,
    UserInUpdate,
)
from src.crud.base import BaseCRUD
from src.securities.hashing.password import password_generator

from src.securities.verification.credentials import credential_verifier

from src.utilities.exceptions.database import (
    EntityAlreadyExists,
    EntityDoesNotExist,
)

from src.utilities.exceptions.password import PasswordDoesNotMatch


class UserCRUD(BaseCRUD):
    async def create_user(self, user_create: UserInCreate) -> UserOutCreate:
        hash_salt = password_generator.generate_salt
        hashed_password = password_generator.generate_hashed_password(
            hash_salt, user_create.password
        )
        new_user = User(
            name=user_create.name,
            hashed_password=hashed_password,
            hash_salt=hash_salt,
            email=user_create.email,
            is_logged_in=False,
        )

        self.async_session.add(instance=new_user)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_user)

        return new_user

    async def read_user_by_username(self, username: str) -> User:
        stmt = sqlalchemy.select(User).where(User.name == username)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(
                "User with username `{username}` does not exist!"
            )

        return query.scalar()  # type: ignore

    async def read_user_by_email(self, email: str) -> User:
        stmt = sqlalchemy.select(User).where(User.email == email)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(
                "User with email `{email}` does not exist!"
            )

        return query.scalar()  # type: ignore

    async def read_user_by_password_authentication(
        self, user_login: UserInLogin
    ) -> User:
        stmt = sqlalchemy.select(User).where(
            User.email == user_login.email,
        )
        query = await self.async_session.execute(statement=stmt)
        db_user = query.scalar()

        if not db_user:
            raise EntityDoesNotExist("Wrong email!")

        if not password_generator.is_password_authenticated(hash_salt=db_user.hash_salt, password=user_login.password, hashed_password=db_user.hashed_password):  # type: ignore
            raise PasswordDoesNotMatch("Password does not match!")

        return db_user  # type: ignore

    async def update_user(self, id: int, user_update: UserInUpdate) -> User:
        new_user_data = dict(user_update)

        select_stmt = sqlalchemy.select(User).where(User.id_user == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_user = query.scalar()

        if not update_user:
            raise EntityDoesNotExist(f"User with id_user `{id}` does not exist!")  # type: ignore

        update_stmt = sqlalchemy.update(table=User).where(User.id_user == update_user.id_user)  # type: ignore

        if new_user_data["name"]:
            update_stmt = update_stmt.values(username=new_user_data["username"])

        if new_user_data["email"]:
            update_stmt = update_stmt.values(username=new_user_data["email"])

        if new_user_data["password"]:
            hash_salt = password_generator.generate_salt
            hashed_password = password_generator.generate_hashed_password(
                hash_salt, update_user.hashed_password
            )
            update_user.hashed_password = hash_salt  # type: ignore
            update_user.hashed_password = hashed_password  # type: ignore

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_user)

        return update_user  # type: ignore

    async def is_username_taken(self, username: str) -> bool:
        username_stmt = (
            sqlalchemy.select(User.name)
            .select_from(User)
            .where(User.name == username)
        )
        username_query = await self.async_session.execute(username_stmt)
        db_username = username_query.scalar()

        if not credential_verifier.is_username_available(username=db_username):
            raise EntityAlreadyExists(f"The username `{username}` is already taken!")  # type: ignore

        return True

    async def is_email_taken(self, email: str) -> bool:
        email_stmt = (
            sqlalchemy.select(User.email)
            .select_from(User)
            .where(User.email == email)
        )
        email_query = await self.async_session.execute(email_stmt)
        db_email = email_query.scalar()

        if not credential_verifier.is_email_available(email=db_email):
            raise EntityAlreadyExists(f"The email `{email}` is already registered!")  # type: ignore

        return True

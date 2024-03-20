import sqlalchemy

from src.data.models import User
from src.data.schemas.user import (
    UserInCreate,
    UserOutCreate,
    UserInUpdate,
    UserWithToken,
)
from src.crud.base import BaseCRUD
from src.securities.hashing.password import password_generator

from src.securities.verification.credentials import credential_verifier

from src.utilities.exceptions.database import (
    EntityAlreadyExists,
    EntityDoesNotExist,
)

from src.utilities.exceptions.password import PasswordDoesNotMatch
from fastapi.security import OAuth2PasswordRequestForm


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
            role_id=user_create.role_id,
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
        self, user_login: OAuth2PasswordRequestForm
    ) -> UserWithToken:
        stmt = sqlalchemy.select(User).where(
            User.email
            == user_login.username,  # This form is expecting username field
        )
        query = await self.async_session.execute(statement=stmt)
        db_user = query.scalar()

        if not db_user:
            raise EntityDoesNotExist("Wrong email!")

        if not password_generator.validate_password(password=user_login.password, hashed_password=db_user.hashed_password):  # type: ignore
            raise PasswordDoesNotMatch("Password does not match!")

        return db_user  # type: ignore

    async def update_user(self, id: int, user_update: UserInUpdate) -> User:
        new_user_data = user_update.model_dump(exclude_none=True)

        select_stmt = sqlalchemy.select(User).where(User.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_user = query.scalar()

        if not update_user:
            raise EntityDoesNotExist(f"User with id `{id}` does not exist!")  # type: ignore

        update_stmt = sqlalchemy.update(table=User).where(User.id == update_user.id)  # type: ignore

        for key in new_user_data:
            if key == "password":
                hash_salt = password_generator.generate_salt
                hashed_password = password_generator.generate_hashed_password(
                    hash_salt, update_user.hashed_password
                )
                update_stmt = update_stmt.values(
                    {"hashed_password": hashed_password},
                    {"hash_salt": hash_salt},
                )

            else:
                update_stmt = update_stmt.values({key: new_user_data[key]})

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

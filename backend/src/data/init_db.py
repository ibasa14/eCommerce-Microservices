# from src.crud.base import ModelType, BaseCRUD
# from src.crud.user import UserCRUD
# from src.data.models import User
# from typing import Dict, Tuple, TypeVar, Type, List
# from src.api.dependencies.repository import get_repository
# from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
# from src.api.dependencies.session import get_async_session

# CrudType = TypeVar("CrudType", bound=BaseCRUD)


# class InitDB:
#     TABLE_NAME_CRUD_TRANSLATOR: Dict[
#         str, Tuple[Type[CrudType], Type[ModelType]] | None
#     ] = {
#         "users": (UserCRUD, User),
#     }

#     @property
#     def users_data(self) -> List[User]:
#         user_1 = {
#             "name": "user1",
#             "email": "email_user1@email.com",
#             "hashed_password": "hashed1",
#             "hash_salt": "hash_salt1",
#             "is_active": True,
#             "is_logged_in": True,
#             "role_id": 1,
#         }
#         user_2 = {
#             "name": "user2",
#             "email": "email_user2@email.com",
#             "hashed_password": "hashed2",
#             "hash_salt": "hash_salt2",
#             "is_active": True,
#             "is_logged_in": True,
#             "role_id": 2,
#         }
#         return [User(**user_1), User(**user_2)]

#     async def _clean_tables(
#         self,
#         *table_names: str | None,
#     ):
#         for table_name in table_names:
#             tuple_param: Tuple[
#                 Type[CrudType], Type[ModelType]
#             ] = self.TABLE_NAME_CRUD_TRANSLATOR.get(table_name)
#             crud_repo: CrudType = tuple_param[0](
#                 anext(get_async_session()), tuple_param[1]
#             )
#             await crud_repo.delete_multiple()

#     async def fill_user_table(self):
#         tuple_param: Tuple[
#             Type[CrudType], Type[ModelType]
#         ] = self.TABLE_NAME_CRUD_TRANSLATOR.get("users")
#         user_crud: UserCRUD = tuple_param[0](get_async_session, tuple_param[1])
#         for user in self.users_data:
#             await user_crud.create_user(user_create=user)


from src.config.manager import settings
from sqlalchemy import create_engine, Engine, text
import pandas as pd


class InitDB:
    def __init__(self):
        self.uri: str = f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/{settings.DB_POSTGRES_NAME}"
        self.engine: Engine = create_engine(self.uri)

    @property
    def users_table(self):
        data = {
            "name": ["user1", "user2"],
            "email": ["email_user1@email.com", "email_user2@email.com"],
            "hashed_password": ["hashed1", "hashed2"],
            "hash_salt": ["hash_salt1", "hash_salt_2"],
            "is_active": [True, True],
            "is_logged_in": [True, True],
            "role_id": [1, 2],
        }
        df = pd.DataFrame(data)
        return df

    def populate_users_table(self):
        with self.engine.connect() as conn:
            conn.execute(text("DELETE FROM users;"))
            self.users_table.to_sql(
                "users", conn, if_exists="append", index=False
            )

from src.config.manager import settings
from sqlalchemy import create_engine
import pandas as pd


class InitDB:
    def __init__(self):
        self.uri = f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/{settings.DB_POSTGRES_NAME}"
        self.engine = create_engine(self.uri)

    @property
    def users_table(self):
        data = {
            "name": ["user1", "user2"],
            "email": ["email_user1@email.com", "email_user2@email.com"],
            "hashed_password": ["hashed1", "hashed2"],
            "has_salt": ["hash_salt1", "hash_salt_2"],
            "is_active": [True, True],
            "is_logged_in": [True, True],
            "role_id": [1, 2],
        }
        df = pd.DataFrame(data)
        return df

    def populate_users_table(self):
        self.users_table.to_sql(
            "users", self.engine, if_exists="replace", index=False
        )

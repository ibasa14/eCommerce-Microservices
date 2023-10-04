from src.config.manager import settings
from sqlalchemy import create_engine, Engine
import pandas as pd
from alembic.config import Config
from alembic import command
from pathlib import Path
import os


class InitDB:
    def __init__(self):
        self.db_uri: str = f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/postgres_testing"
        self.engine: Engine = create_engine(self.db_uri)
        self.alembic_directory = os.path.join(
            Path(__file__).parent.parent.parent.resolve(), "alembic"
        )
        self.ini_path = os.path.join(
            Path(__file__).parent.parent.parent.resolve(), "alembic.ini"
        )
        self._clean_db_to_definition()

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

    @property
    def products_table(self):
        data = {
            "name": ["product1", "product2"],
            "picture": ["not_defined.png"] * 2,
            "description": ["description1", "description2"],
            "price": [59.99, 22],
            "stock": [100, 5],
            "category_id": [1, 2],
        }
        df = pd.DataFrame(data)
        return df

    def _clean_db_to_definition(self) -> None:
        alembic_cfg = Config(self.ini_path)
        alembic_cfg.set_main_option("script_location", self.alembic_directory)
        alembic_cfg.set_main_option("sqlalchemy.url", self.db_uri)
        with self.engine.begin() as conn:
            alembic_cfg.attributes["connection"] = conn
            command.downgrade(alembic_cfg, "base")
            command.upgrade(alembic_cfg, "head")

    def populate_db(self):
        with self.engine.begin() as conn:
            # populate users
            self.users_table.to_sql(
                "users", conn, if_exists="append", index=False
            )
            # populate products
            self.products_table.to_sql(
                "products", conn, if_exists="append", index=False
            )

from src.config.manager import settings
from sqlalchemy import create_engine, Engine
from sqlalchemy_utils import database_exists, create_database, drop_database
import pandas as pd
from alembic.config import Config
from alembic import command
from pathlib import Path
import os
from src.securities.hashing.password import password_generator


class InitDB:
    def __init__(self):
        self.db_uri: str = (
            f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/postgres_account_testing"
        )
        if database_exists(self.db_uri): drop_database(self.db_uri)
        create_database(self.db_uri)
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
            "id": [2, 3],
            "name": ["test_user", "test_user_admin"],
            "email": ["test_user@ibc.com", "test_user_admin@ibc.com"],
            "hashed_password": [
                password_generator.generate_hashed_password("test_password")
            ]
            * 2,
            "is_active": [True] * 2,
            "is_logged_in": [False] * 2,
            "role_id": [2, 1],
        }
        df = pd.DataFrame(data)
        return df

    def _clean_db_to_definition(self) -> None:
        alembic_cfg = Config(self.ini_path)
        alembic_cfg.set_main_option("script_location", self.alembic_directory)
        alembic_cfg.set_main_option("sqlalchemy.url", self.db_uri)
        with self.engine.begin() as conn:
            alembic_cfg.attributes["connection"] = conn
            # command.downgrade(alembic_cfg, "base")
            command.upgrade(alembic_cfg, "head")

    def populate_db(self):
        with self.engine.begin() as conn:
            # populate users
            self.users_table.to_sql(
                "users", conn, if_exists="append", index=False
            )

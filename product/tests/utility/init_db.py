from src.config.manager import settings
from sqlalchemy import create_engine, Engine
from sqlalchemy_utils import database_exists, create_database, drop_database
import pandas as pd
from alembic.config import Config
from alembic import command
from pathlib import Path
import os


class InitDB:
    def __init__(self):
        self.db_uri: str = (
            f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/postgres_product_testing"
        )
        if database_exists(self.db_uri):
            drop_database(self.db_uri)
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
    def products_table(self):
        data = {
            "name": ["product1", "product2", "product_22"],
            "picture": ["not_defined.png"] * 3,
            "description": ["description1", "description2", "description22"],
            "price": [59.99, 22, 92.59],
            "stock": [100, 5, 200],
            "category_id": [1, 2, 3],
        }
        df = pd.DataFrame(data)
        return df

    def _clean_db_to_definition(self) -> None:
        alembic_cfg = Config(self.ini_path)
        alembic_cfg.set_main_option("script_location", self.alembic_directory)
        alembic_cfg.set_main_option("sqlalchemy.url", self.db_uri)
        with self.engine.begin() as conn:
            alembic_cfg.attributes["connection"] = conn
            command.upgrade(alembic_cfg, "head")

    def populate_db(self):
        with self.engine.begin() as conn:
            # populate products
            self.products_table.to_sql(
                "products", conn, if_exists="append", index=False
            )

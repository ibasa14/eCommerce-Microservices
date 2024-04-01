import datetime
import os
from pathlib import Path

import pandas as pd
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from src.config.manager import settings


class InitDB:
    def __init__(self):
        self.db_uri: str = f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/postgres_order_testing"
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
    def orders_table(self):
        # First order from 2, with 1 product1, 2 product 2
        # Second order from 3 with 5 product 3
        data = {
            "user_id": [2, 3],
            "date": [
                datetime.datetime(2024, 3, 24, 10, 10),
                datetime.datetime(2024, 3, 24, 11, 10),
            ],
            "total_price": [55.99 * 1 + 2 * 22, 5 * 92.59],
        }
        df = pd.DataFrame(data)
        return df

    @property
    def order_details_table(self):
        data = {
            "quantity": [1, 2, 5],
            "total": [55.99 * 1, 2 * 22, 5 * 92.59],
            "order_id": [1, 1, 2],
            "product_id": [1, 2, 3],
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
            # populate orders
            self.orders_table.to_sql(
                "orders", conn, if_exists="append", index=False
            )
            self.order_details_table.to_sql(
                "order_details", conn, if_exists="append", index=False
            )

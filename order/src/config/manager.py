import typing
from functools import lru_cache

import decouple

from src.config.settings.base import OrderBaseSettings
from src.config.settings.development import OrderDevSettings
from src.config.settings.environment import Environment
from src.config.settings.production import OrderProdSettings
from src.config.settings.staging import OrderStageSettings


class OrderSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    @classmethod
    def get_env_settings(
        cls, environment: str
    ) -> typing.Union[OrderDevSettings, OrderProdSettings, OrderStageSettings]:
        if environment == Environment.DEVELOPMENT.value:
            return OrderDevSettings
        elif environment == Environment.STAGING.value:
            return OrderStageSettings
        return OrderProdSettings


@lru_cache()
def get_settings() -> OrderBaseSettings:
    return OrderSettingsFactory.get_env_settings(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))()  # type: ignore


settings: OrderBaseSettings = get_settings()

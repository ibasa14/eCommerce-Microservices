import typing
from functools import lru_cache

import decouple
from src.config.settings.base import ProductBaseSettings
from src.config.settings.development import ProductDevSettings
from src.config.settings.environment import Environment
from src.config.settings.production import ProductProdSettings
from src.config.settings.staging import ProductStageSettings


class ProductSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    @classmethod
    def get_env_settings(
        cls, environment: str
    ) -> typing.Union[
        ProductDevSettings, ProductProdSettings, ProductStageSettings
    ]:
        if environment == Environment.DEVELOPMENT.value:
            return ProductDevSettings
        elif environment == Environment.STAGING.value:
            return ProductStageSettings
        return ProductProdSettings


@lru_cache()
def get_settings() -> ProductBaseSettings:
    return ProductSettingsFactory.get_env_settings(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))()  # type: ignore


settings: ProductBaseSettings = get_settings()

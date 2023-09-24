import typing
from functools import lru_cache

import decouple

from src.config.settings.base import BackendBaseSettings
from src.config.settings.development import BackendDevSettings
from src.config.settings.environment import Environment
from src.config.settings.production import BackendProdSettings
from src.config.settings.staging import BackendStageSettings


class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    @classmethod
    def get_env_settings(
        cls, environment: str
    ) -> typing.Any[
        BackendDevSettings, BackendProdSettings, BackendStageSettings
    ]:
        if environment == Environment.DEVELOPMENT.value:
            return BackendDevSettings()
        elif environment == Environment.STAGING.value:
            return BackendStageSettings()
        return BackendProdSettings()


@lru_cache()
def get_settings() -> BackendBaseSettings:
    return BackendSettingsFactory.get_env_settings(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))()  # type: ignore


settings: BackendBaseSettings = get_settings()

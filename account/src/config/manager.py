import typing
from functools import lru_cache

import decouple
from src.config.settings.base import AuthenticationBaseSettings
from src.config.settings.development import AuthenticationDevSettings
from src.config.settings.environment import Environment
from src.config.settings.production import AuthenticationProdSettings
from src.config.settings.staging import AuthenticationStageSettings


class AuthenticationSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    @classmethod
    def get_env_settings(
        cls, environment: str
    ) -> typing.Union[
        AuthenticationDevSettings,
        AuthenticationProdSettings,
        AuthenticationStageSettings,
    ]:
        if environment == Environment.DEVELOPMENT.value:
            return AuthenticationDevSettings
        elif environment == Environment.STAGING.value:
            return AuthenticationStageSettings
        return AuthenticationProdSettings


@lru_cache()
def get_settings() -> AuthenticationBaseSettings:
    return AuthenticationSettingsFactory.get_env_settings(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))()  # type: ignore


settings: AuthenticationBaseSettings = get_settings()

from src.config.settings.base import AuthenticationBaseSettings
from src.config.settings.environment import Environment


class AuthenticationStageSettings(AuthenticationBaseSettings):
    DESCRIPTION: str | None = "Test Environment."

    ENVIRONMENT: Environment = Environment.STAGING

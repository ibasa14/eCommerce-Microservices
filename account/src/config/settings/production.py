from src.config.settings.base import AuthenticationBaseSettings
from src.config.settings.environment import Environment


class AuthenticationProdSettings(AuthenticationBaseSettings):
    DESCRIPTION: str | None = "Production Environment."
    ENVIRONMENT: Environment = Environment.PRODUCTION

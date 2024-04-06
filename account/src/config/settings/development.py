from src.config.settings.base import AuthenticationBaseSettings
from src.config.settings.environment import Environment


class AuthenticationDevSettings(AuthenticationBaseSettings):
    DESCRIPTION: str | None = "Development Environment."

    ENVIRONMENT: Environment = Environment.DEVELOPMENT

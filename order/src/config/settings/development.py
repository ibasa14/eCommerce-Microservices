from src.config.settings.base import OrderBaseSettings
from src.config.settings.environment import Environment


class OrderDevSettings(OrderBaseSettings):
    DESCRIPTION: str | None = "Development Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

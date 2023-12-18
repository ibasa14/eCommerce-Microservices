from src.config.settings.base import ProductBaseSettings
from src.config.settings.environment import Environment


class ProductDevSettings(ProductBaseSettings):
    DESCRIPTION: str | None = "Development Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

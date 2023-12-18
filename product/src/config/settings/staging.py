from src.config.settings.base import ProductBaseSettings
from src.config.settings.environment import Environment


class ProductStageSettings(ProductBaseSettings):
    DESCRIPTION: str | None = "Test Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.STAGING

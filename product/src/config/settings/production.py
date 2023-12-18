from src.config.settings.base import ProductBaseSettings
from src.config.settings.environment import Environment


class ProductProdSettings(ProductBaseSettings):
    DESCRIPTION: str | None = "Production Environment."
    ENVIRONMENT: Environment = Environment.PRODUCTION

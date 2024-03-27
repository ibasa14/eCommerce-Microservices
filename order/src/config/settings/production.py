from src.config.settings.base import OrderBaseSettings
from src.config.settings.environment import Environment


class OrderProdSettings(OrderBaseSettings):
    DESCRIPTION: str | None = "Orderion Environment."
    ENVIRONMENT: Environment = Environment.PRODUCTION

from src.config.settings.base import OrderBaseSettings
from src.config.settings.environment import Environment


class OrderStageSettings(OrderBaseSettings):
    DESCRIPTION: str | None = "Test Environment."

    ENVIRONMENT: Environment = Environment.STAGING

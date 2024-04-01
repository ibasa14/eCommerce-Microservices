import logging

import pydantic_settings
from decouple import config


class OrderBaseSettings(pydantic_settings.BaseSettings):
    TITLE: str = "IBC project - Orders"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC+1"
    DESCRIPTION: str | None = None

    SERVER_HOST: str = config("SERVER_HOST", cast=str)  # type: ignore
    SERVER_PORT: int = config("SERVER_PORT", cast=int)  # type: ignore
    SERVER_WORKERS: int = config("SERVER_WORKERS", cast=int)  # type: ignore
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    DB_POSTGRES_HOST: str = config("POSTGRES_HOST", cast=str)  # type: ignore
    DB_MAX_POOL_CON: int = config("DB_MAX_POOL_CON", cast=int)  # type: ignore
    DB_POSTGRES_NAME: str = config("POSTGRES_DB", cast=str)  # type: ignore
    DB_POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str)  # type: ignore
    DB_POOL_SIZE: int = config("DB_POOL_SIZE", cast=int)  # type: ignore
    DB_POOL_OVERFLOW: int = config("DB_POOL_OVERFLOW", cast=int)  # type: ignore
    DB_POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int)  # type: ignore
    DB_POSTGRES_SCHEMA: str = config("POSTGRES_SCHEMA", cast=str)  # type: ignore
    DB_TIMEOUT: int = config("DB_TIMEOUT", cast=int)  # type: ignore
    DB_POSTGRES_USERNAME: str = config("POSTGRES_USERNAME", cast=str)  # type: ignore

    IS_DB_ECHO_LOG: bool = config("IS_DB_ECHO_LOG", cast=bool)  # type: ignore
    IS_DB_FORCE_ROLLBACK: bool = config("IS_DB_FORCE_ROLLBACK", cast=bool)  # type: ignore
    IS_DB_EXPIRE_ON_COMMIT: bool = config("IS_DB_EXPIRE_ON_COMMIT", cast=bool)  # type: ignore

    API_TOKEN: str = config("API_TOKEN", cast=str)  # type: ignore
    AUTH_TOKEN: str = config("AUTH_TOKEN", cast=str)  # type: ignore
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)  # type: ignore
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", cast=str)  # type: ignore
    JWT_MIN: int = config("JWT_MIN", cast=int)  # type: ignore
    JWT_HOUR: int = config("JWT_HOUR", cast=int)  # type: ignore
    JWT_DAY: int = config("JWT_DAY", cast=int)  # type: ignore
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = JWT_MIN * JWT_HOUR * JWT_DAY

    IS_ALLOWED_CREDENTIALS: bool = config("IS_ALLOWED_CREDENTIALS", cast=bool)  # type: ignore
    ALLOWED_ORIGINS: list[str] = []
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    PRODUCT_PORT: str = config("PRODUCT_PORT", cast=str)  # type: ignore
    PRODUCT_HOST: str = config("PRODUCT_HOST", cast=str)  # type: ignore

    AUTHENTICATION_PORT: str = config("AUTHENTICATION_PORT", cast=str)  # type: ignore
    AUTHENTICATION_PORT_EXT: str = config("AUTHENTICATION_PORT_EXT", cast=str)  # type: ignore
    AUTHENTICATION_HOST: str = config("AUTHENTICATION_HOST", cast=str)  # type: ignore
    AUTHENTICATION_ROUTER: str = config("AUTHENTICATION_ROUTER", cast=str)  # type: ignore
    AUTHENTICATION_ENDPOINT: str = config("AUTHENTICATION_ENDPOINT", cast=str)  # type: ignore
    AUTHENTICATION_URL: str = f"http://{AUTHENTICATION_HOST}:{AUTHENTICATION_PORT_EXT}/api{AUTHENTICATION_ROUTER}{AUTHENTICATION_ENDPOINT}"

    @property
    def set_order_app_attributes(self) -> dict[str, str | bool | None]:
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }

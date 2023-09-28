import asgi_lifespan
import fastapi
import httpx
import pytest
from fastapi.testclient import TestClient
from src.main import initialize_backend_application
# from src.data.init_db import InitDB


# @pytest.fixture(scope="session")
# def test_db() -> None:
#     InitDB().populate_users_table()


@pytest.fixture(scope = "session")
def backend_test_app() -> fastapi.FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """

    return initialize_backend_application()


# @pytest.fixture(name="initialize_backend_test_application")
# async def initialize_backend_test_application(backend_test_app: fastapi.FastAPI) -> fastapi.FastAPI:  # type: ignore
#     async with asgi_lifespan.LifespanManager(backend_test_app):
#         yield backend_test_app


# @pytest.fixture(name="async_client")
# async def async_client(initialize_backend_test_application: fastapi.FastAPI) -> httpx.AsyncClient:  # type: ignore
#     async with httpx.AsyncClient(
#         app=initialize_backend_test_application,
#         headers={"Content-Type": "application/json"},
#     ) as client:
#         yield client

@pytest.fixture(scope="session")
def sync_client(backend_test_app: fastapi.FastAPI) -> TestClient:  # type: ignore
    return TestClient(backend_test_app)
import asgi_lifespan
import fastapi
import httpx
import pytest
from fastapi.testclient import TestClient
from src.main import initialize_backend_application
import asyncio
from src.data.init_db import InitDB
from src.config.manager import settings


# NOTE: this is required to prevent ScopeMismatch error
@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def test_db() -> None:
    init_db = InitDB()
    init_db.clean_users_table()
    init_db.populate_users_table()


@pytest.fixture(scope="session")
def api_url() -> str:
    return f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}{settings.API_PREFIX}"


@pytest.fixture(scope="session")
def backend_test_app() -> fastapi.FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """

    return initialize_backend_application()


@pytest.fixture(name="initialize_backend_test_application")
async def initialize_backend_test_application(backend_test_app: fastapi.FastAPI) -> fastapi.FastAPI:  # type: ignore
    async with asgi_lifespan.LifespanManager(backend_test_app):
        yield backend_test_app


@pytest.fixture(name="async_client")
async def async_client(initialize_backend_test_application: fastapi.FastAPI) -> httpx.AsyncClient:  # type: ignore
    async with httpx.AsyncClient(
        app=initialize_backend_test_application,
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture(scope="session")
def sync_client(backend_test_app: fastapi.FastAPI) -> TestClient:  # type: ignore
    return TestClient(backend_test_app)

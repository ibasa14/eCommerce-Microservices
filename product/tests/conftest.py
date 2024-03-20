import asgi_lifespan
import fastapi
import httpx
import pytest
from src.main import initialize_product_application
import asyncio
from tests.utility.init_db import InitDB
from src.config.manager import settings
from src.api.dependencies.session import get_async_session
from tests.utility.session import get_async_session_testing


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
    init_db.populate_db()


@pytest.fixture(scope="session")
def api_url() -> str:
    return f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}{settings.API_PREFIX}"


@pytest.fixture(scope="session")
def product_test_app() -> fastapi.FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """
    testing_app = initialize_product_application()
    testing_app.dependency_overrides[
        get_async_session
    ] = get_async_session_testing
    return testing_app


@pytest.fixture(scope="session")
async def async_client(product_test_app: fastapi.FastAPI) -> httpx.AsyncClient:  # type: ignore
    async with asgi_lifespan.LifespanManager(product_test_app):
        async with httpx.AsyncClient(
            app=product_test_app,
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client

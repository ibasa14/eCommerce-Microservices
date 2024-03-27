import asgi_lifespan
import fastapi
import httpx
import pytest
from src.main import initialize_order_application
import asyncio
from tests.utility.init_db import InitDB
from src.config.manager import settings
from src.api.dependencies.session import get_async_session
from tests.utility.session import get_async_session_testing
from tests.utility.token import TEST_USER_TOKEN, TEST_USER_ADMIN_TOKEN


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
def order_test_app() -> fastapi.FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """
    testing_app = initialize_order_application()
    testing_app.dependency_overrides[
        get_async_session
    ] = get_async_session_testing
    return testing_app


@pytest.fixture(scope="session")
async def async_authenticated_client(order_test_app: fastapi.FastAPI) -> httpx.AsyncClient:  # type: ignore
    async with asgi_lifespan.LifespanManager(order_test_app):
        async with httpx.AsyncClient(
            app=order_test_app,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {TEST_USER_TOKEN}",
            },
        ) as client:
            yield client


@pytest.fixture(scope="session")
async def async_authenticated_client_admin(order_test_app: fastapi.FastAPI) -> httpx.AsyncClient:  # type: ignore
    async with asgi_lifespan.LifespanManager(order_test_app):
        async with httpx.AsyncClient(
            app=order_test_app,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {TEST_USER_ADMIN_TOKEN}",
            },
        ) as client:
            yield client


@pytest.fixture(scope="session")
async def async_non_authenticated_client(order_test_app: fastapi.FastAPI) -> httpx.AsyncClient:  # type: ignore
    async with asgi_lifespan.LifespanManager(order_test_app):
        async with httpx.AsyncClient(
            app=order_test_app,
            headers={
                "Content-Type": "application/json",
            },
        ) as client:
            yield client

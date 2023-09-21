import fastapi
import pytest
from fastapi.testclient import TestClient

from src.main import initialize_backend_application


@pytest.fixture(name="backend_test_client")
def backend_test_client() -> TestClient:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """

    return TestClient(initialize_backend_application())

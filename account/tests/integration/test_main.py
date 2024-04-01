import fastapi
import src
from src.main import app


def test_src_version() -> None:
    assert src.__version__ == "0.0.1"


def test_application_is_fastapi_instance() -> None:
    assert isinstance(app, fastapi.FastAPI)
    assert app.redoc_url == "/redoc"
    assert app.docs_url == "/docs"
    assert app.openapi_url == "/openapi.json"
    assert app.redoc_url == "/redoc"

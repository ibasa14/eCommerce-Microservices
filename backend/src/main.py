import fastapi
from fastapi.middleware.cors import CORSMiddleware

from src.api.endpoints import router as api_endpoint_router

# from src.config.events import execute_backend_server_event_handler, terminate_backend_server_event_handler
from src.config.manager import settings


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI(**settings.set_backend_app_attributes)  # type: ignore

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    # app.add_event_handler(
    #     "startup",
    #     execute_backend_server_event_handler(app=app),
    # )
    # app.add_event_handler(
    #     "shutdown",
    #     terminate_backend_server_event_handler(app=app),
    # )

    app.include_router(router=api_endpoint_router, prefix=settings.API_PREFIX)

    return app


app: fastapi.FastAPI = initialize_backend_application()

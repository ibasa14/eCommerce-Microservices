import uvicorn

from src.main import app
from src.config.manager import settings

if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )

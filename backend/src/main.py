import fastapi
import uvicorn


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI()  # type: ignore
    return app


app: fastapi.FastAPI = initialize_backend_application()


@app.get("/hello_world")
def hello_world():
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run(app="main.app")

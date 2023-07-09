import os

if __name__ == "__main__":
    import uvicorn

    from app.main import app

    uvicorn.run(
        app, port=8100, log_level=os.getenv("UVICORN_LOG_LEVEL", "debug")
    )

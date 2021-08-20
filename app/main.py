import logging

from fastapi import FastAPI

from app.services.db import init_db
from app.core.config import Settings, get_settings


log = logging.getLogger("uvicorn.info")


settings: Settings = get_settings()


def create_application() -> FastAPI:
    application = FastAPI(
            title=settings.WEB_APP_TITLE,
            description=settings.WEB_APP_DESCRIPTION,
            version=settings.WEB_APP_VERSION
        )
    return application


app = create_application()

@app.get("/")
def index():
    return {"detail": "index guane app"}


@app.on_event("startup")
async def startup_event():
    init_db(app)
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")

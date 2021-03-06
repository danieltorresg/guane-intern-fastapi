import logging
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings, EmailStr

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    WEB_APP_TITLE: str
    WEB_APP_DESCRIPTION: str
    WEB_APP_VERSION: str
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: AnyUrl
    IMAGE_API: str
    INITIAL_EMAIL: EmailStr = "init@mail.com"
    INITIAL_PASSWORD: str = "SecurePassword"


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()

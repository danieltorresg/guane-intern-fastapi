import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from tortoise import Tortoise
from tortoise.contrib.test import initializer, finalizer

from app.main import app
from app.services.db import init_db


from app.core.config import Settings, get_settings

settings: Settings = get_settings()




# async def override_init_db(request):
#     db_url = settings.DATABASE_TEST_URL
#     initializer(["app.infra.postgres.models"], db_url=db_url)
#     request.addfinalizer(finalizer)

    # await Tortoise.init(
    #     db_url=db_url,
    #     modules={"models": ["app.infra.postgres.models"]},
    #     _create_db = create_db        
    # )
    # if create_db:
    #     print("database created")
    # if schemas:
    #     await Tortoise.generate_schemas()
    #     print("schemas generated")


# @pytest.fixture(scope="function")
# def init_sqldb():
#     app.dependency_overrides[init_db] = override_init_db(create_db=True, schemas=True)
#     client = TestClient(app)
#     yield client


@pytest.fixture(scope="session", autouse=True)
def initialize_test(request):
    db_url = settings.DATABASE_TEST_URL
    initializer(["app.infra.postgres.models"], db_url=db_url)
    request.addfinalizer(finalizer)

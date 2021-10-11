import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.config import Settings, get_settings
from app.main import app

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


@pytest.fixture(scope="function")
def test_app():
    cliente = TestClient(app)
    return cliente


@pytest.fixture(scope="function", autouse=True)  # session y function
def initialize_test(request):
    db_url = settings.DATABASE_TEST_URL
    initializer(["app.infra.postgres.models"], db_url=db_url)
    request.addfinalizer(finalizer)

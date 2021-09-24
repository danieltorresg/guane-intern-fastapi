import pytest
from starlette.testclient import TestClient

from tests.utils import create_user, authenticate

endpoint = "/api/v1/login/token"

user_standard = {
        "id": 8,
        "name": "Mario",
        "last_name": "Gutierrez",
        "email": "mario@mail.com",
        "password": "hola",
        "is_active": True,
}


some_data_login = [
    {
        "username": "invalid@mail.com",
        "password": user_standard["password"]
    },
    {
        "username": user_standard["email"],
        "password": "invalid_password"
    },
    {
        "username": "invalid@mail.com",
        "password": "invalid_password"
    }
]

def test_login(test_app: TestClient):
    url = endpoint
    
    response_create = create_user(test_app, "/api/v1/users", user_standard)
    assert response_create.status_code == 200
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app, url, data_login)
    assert response_login.status_code == 200, response_login.text
    assert response_login.json()["access_token"] == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hcmlvQG1haWwuY29tIiwiaWQiOjh9.e3hMlvp_ydcXffGK9_jOxSePDZGXl2hWibvgCWupCR8"


@pytest.mark.parametrize("data", [
    pytest.param(some_data_login[0], marks=[pytest.mark.dependency(name="invalid_username")]),
    pytest.param(some_data_login[1], marks=[pytest.mark.dependency(name="invalid_password")]),
    pytest.param(some_data_login[2], marks=[pytest.mark.dependency(name="all_invalid")]),
])
def test_login_invalid_data(test_app: TestClient, data: dict):
    url = endpoint
    response_create = create_user(test_app, "/api/v1/users", user_standard)
    assert response_create.status_code == 200
    response_login = authenticate(test_app, url, data)
    assert response_login.status_code == 400, response_login.text
    assert response_login.json() == {"detail": "Incorrect email or password"}


from fastapi.testclient import TestClient

from app.main import app
from tests.utils import create_user

client = TestClient(app)

endpoint = "/api/v1/login/token"

def test_login():
    url = endpoint
    user = {
        "id": 8,
        "name": "Mario",
        "last_name": "Gutierrez",
        "email": "mario@mail.com",
        "password": "hola",
        "is_active": True,
    }
    response_create = create_user("/api/v1/users", user)
    assert response_create.status_code == 200
    data_login = {
        "username": user["email"],
        "password": user["password"]
    }
    response_login = authenticate(endpoint, data_login)
    assert response_login.status_code == 200, response_login.text
    assert response_login.json()["access_token"] == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hcmlvQG1haWwuY29tIiwiaWQiOjh9.e3hMlvp_ydcXffGK9_jOxSePDZGXl2hWibvgCWupCR8"

def authenticate(url, data):
    return client.post(url, data=data)

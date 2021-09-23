from fastapi.testclient import TestClient

from app.main import app
from tests.utils import create_user
from tests.test_login import authenticate

client = TestClient(app)

endpoint = "/api/v1/dogs"

def test_create_dog():
    url = endpoint+"/Estrella"
    user = {
        "id": 9,
        "name": "Julian",
        "last_name": "Gomez",
        "email": "jul@mail.com",
        "password": "hola",
        "is_active": True,
    }
    response_create = create_user("/api/v1/users", user)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user["email"],
        "password": user["password"]
    }
    data_dog = {
        "id": 0
    }
    response_login = authenticate("/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    response = client.post(url, headers=headers, json=data_dog)
    assert response.status_code == 200, response.text
    assert response.json()["id"] == data_dog["id"]
    assert response.json()["name"] == "Estrella"
    assert response.json()["in_charge_id"] == user["id"]
    
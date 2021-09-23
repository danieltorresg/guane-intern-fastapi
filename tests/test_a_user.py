import pytest

from fastapi.testclient import TestClient
from app.core.security import verify_password

from app.main import app
from tests.utils import create_user

client = TestClient(app)

endpoint = "/api/v1/users"


"""" Es un 200 y retornar un arreglo vacio """

def test_get_users_empty():
    url = endpoint
    response = client.get(url)
    assert response.status_code == 404
    assert response.json() == {"detail": "Users not found"}


def test_create_user():
    url = endpoint
    data = {
        "id": 2,
        "name": "Daniel",
        "last_name": "Torres",
        "email": "dan@mail.com",
        "password": "hola",
        "is_active": True,
    }
    response = create_user(endpoint, data)
    assert response.status_code == 200
    assert response.json()["id"] == data["id"]
    assert response.json()["name"] == data["name"]
    assert response.json()["last_name"] == data["last_name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["is_active"] == data["is_active"]
    assert verify_password(data["password"],response.json()["password"])


def test_get_uploadfile():
    url = endpoint+"/upload_file"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"filename": "guane_file.txt"}


def test_deactivate_user():
    url = endpoint+"/deactivate?id=3"
    user = {
        "id": 3,
        "name": "Daniel",
        "last_name": "Torres",
        "email": "daniel@mail.com",
        "password": "hola",
        "is_active": True,
    }
    response1 = create_user(endpoint, user)
    assert response1.status_code == 200, response1.text
    response = client.put(url)
    assert response.status_code == 200, response.text
    assert response.json()["id"] == 3
    assert response.json()["name"] == "Daniel"
    assert response.json()["last_name"] == "Torres"
    assert response.json()["email"] == "daniel@mail.com"
    assert response.json()["is_active"] == False
    assert response.json()["created_date"]
    assert verify_password("hola",response.json()["password"])


def test_get_user_by_id():
    url = endpoint+"/4"
    user = {
        "id": 4,
        "name": "Leidy",
        "last_name": "Torres",
        "email": "leidy@mail.com",
        "password": "hola",
        "is_active": True,
    }
    create_user(endpoint, user)
    response = client.get(url)
    assert response.status_code == 200, response.text
    assert response.json()["id"] == user["id"]
    assert response.json()["name"] == user["name"]
    assert response.json()["last_name"] == user["last_name"]
    assert response.json()["email"] == user["email"]
    assert response.json()["is_active"] == True
    assert response.json()["created_date"]
    assert verify_password(user["password"],response.json()["password"])


def test_update_user():
    url = endpoint+"/5"
    user = {
        "id": 5,
        "name": "Meliza",
        "last_name": "Torres",
        "email": "mel@mail.com",
        "password": "hola",
        "is_active": True,
    }
    update_user = {
        "name": "Leidy",
        "last_name": "Gonzalez",
        "email": "micorreo@mail.com",
    }
    create_user(endpoint, user)
    response = client.put(url, json=update_user)
    assert response.json()["id"] == user["id"]
    assert response.json()["name"] != user["name"]
    assert response.json()["last_name"] != user["last_name"]
    assert response.json()["email"] != user["email"]
    assert response.json()["created_date"]


def test_delete_user():
    url = endpoint+"/6"
    user = {
        "id": 6,
        "name": "Jefferson",
        "last_name": "Gutierritos",
        "email": "jefgu@mail.com",
        "password": "hola",
        "is_active": True,
    }
    create_user(endpoint, user)
    response = client.delete(url)
    assert response.json()["id"] == user["id"]
    assert response.json()["name"] == user["name"]
    assert response.json()["last_name"] == user["last_name"]
    assert response.json()["email"] == user["email"]
    assert response.json()["is_active"] == True
    assert response.json()["created_date"]
    assert verify_password(user["password"],response.json()["password"])


def test_get_users():
    data = {
        "id": 2,
        "name": "Daniel",
        "last_name": "Torres",
        "email": "dan@mail.com",
        "is_active": True,
    }
    url = endpoint
    response = client.get(url)
    first_user = response.json()[0]    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert isinstance(response.json()[0], dict)
    assert first_user["id"] == 2
    assert first_user["name"] == "Daniel"
    assert first_user["last_name"] == "Torres"
    assert first_user["email"] == "dan@mail.com"
    assert first_user["is_active"] == True
    assert first_user["created_date"]
    assert verify_password("hola",first_user["password"])



    


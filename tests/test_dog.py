import pytest

from starlette.testclient import TestClient

from tests.utils import create_user, create_dog
from tests.test_login import authenticate


endpoint = "/api/v1/dogs"


user_standard = {
    "id": 2,
    "name": "Daniel",
    "last_name": "Torres",
    "email": "daniel@mail.com",
    "password": "hola",
    "is_active": True,
}

dog_same_id = {
    "Chispas":
    {
        "id": 1,
        "owner_email": user_standard["email"]
    }
}

dog_same_name = {
    "Estrella":
    {
        "id": 2,
        "owner_email": user_standard["email"]
    }
}


some_dogs = {
        "Estrella":{
            "id": 1,
            "owner_email": user_standard["email"]
        },
        "Chispas":{
            "id": 2,
            "owner_email": user_standard["email"]
        },
        "Rayo":{
            "id": 3
        },
}

updates = [
    {
        "name": "Luna"
    },
    {
        "picture": "new_photo"
    },
    {
        "name": "Luna",
        "picture": "new_photo"
    },
]
def test_get_dogs_empty(test_app: TestClient):
    url = endpoint
    response = test_app.get(url)
    assert response.status_code == 404
    assert response.json() == {"detail": "Dogs not found"}


@pytest.mark.parametrize("some_dogs", [
    pytest.param(some_dogs, marks=[pytest.mark.dependency(name="dogs_full")])
])
def test_get_dogs_full(test_app: TestClient, some_dogs: list):
    url = endpoint
    response_create = create_user(test_app,"/api/v1/users", user_standard)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app,"/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    for name, data in some_dogs.items():
        response = create_dog(test_app, endpoint+f"/{name}", headers, data)
        assert response.status_code >= 200 and response.status_code < 300, response.text
    response = test_app.get(url) 
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)
    assert isinstance(response.json()[0], dict)
    assert response.json()[0]["name"] == "Estrella"


@pytest.mark.parametrize("some_dogs", [
    pytest.param(some_dogs, marks=[pytest.mark.dependency(name="dogs_adopted")])
])
def test_is_adopted(test_app: TestClient, some_dogs: dict):
    url = endpoint+"/is_adopted"
    response_create = create_user(test_app,"/api/v1/users", user_standard)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app,"/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    for name, data in some_dogs.items():
        response_dog = create_dog(test_app, endpoint+f"/{name}", headers, data)
        assert response_dog.status_code >= 200 and response_dog.status_code < 300, response_dog.text
        assert response_dog.json()["in_charge_id"] == user_standard["id"]
    response_adopted = test_app.get(url)
    assert response_adopted.status_code ==200
    assert isinstance(response_adopted.json(), list)
    assert len(response_adopted.json()) == 2
    assert isinstance(response_adopted.json()[0], dict)


def test_adopt(test_app: TestClient):
    url = endpoint+"/adopt/Chispas"
    response_create = create_user(test_app, "/api/v1/users", user_standard)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app, "/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    data_dog = {
        "id": 2
    }
    response_dog = create_dog(test_app, "/api/v1/dogs/Chispas", headers, data_dog)
    assert response_dog.json()["in_charge_id"] == user_standard["id"]
    assert response_dog.json()["is_adopted"] == False
    response_adopt = test_app.put(f"{url}?owner_email={user_standard['email']}", headers=headers)
    assert response_adopt.status_code == 200, response_adopt.text


@pytest.mark.parametrize("some_dogs", [
    pytest.param(some_dogs, marks=[pytest.mark.dependency(name="create_dogs")])
])
def test_create_dog(test_app: TestClient, some_dogs: dict):
    url = endpoint
    response_create = create_user(test_app, "/api/v1/users", user_standard)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app, "/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    for name, data in some_dogs.items():
        response_dog = create_dog(test_app, url+f"/{name}", headers, data)
        assert response_dog.status_code >= 200 and response_dog.status_code < 300, response_dog.text
        assert response_dog.json()["id"] == data["id"]
        assert response_dog.json()["name"] == name
        assert response_dog.json()["in_charge_id"] == user_standard["id"]



@pytest.mark.parametrize("some_dogs", [
    pytest.param(dog_same_id, marks=[pytest.mark.dependency(name="create_same_id_dog")]),
    pytest.param(dog_same_name, marks=[pytest.mark.dependency(name="create_same_name_dog")]),
])
def test_create_duplicate_dog(test_app: TestClient, some_dogs: dict):
    url = endpoint
    data_dog = {
        "id": 1,
        "owner_email": user_standard["email"]
    }
    response_create = create_user(test_app, "/api/v1/users", user_standard)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app, "/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    response_dog = create_dog(test_app, url+"/Estrella", headers, data_dog)
    assert response_dog.status_code >= 200 and response_dog.status_code < 300, response_dog.text

    for name, data in some_dogs.items():
        response_duplicate = create_dog(test_app, url+f"/{name}", headers, data)
        assert response_duplicate.status_code >= 400 and response_duplicate.status_code < 500, response_duplicate.text
        assert response_duplicate.json() == {"detail": "Duplicate key: There is a dog with this data"}


def test_get_dog_by_name(test_app: TestClient):
    url = endpoint+"/Estrella"
    data_dog = {
        "id": 1,
        "owner_email": user_standard["email"]
    }
    response_create = create_user(test_app, "/api/v1/users", user_standard)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app, "/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    response_dog = create_dog(test_app, url, headers, data_dog)
    assert response_dog.status_code >= 200 and response_dog.status_code < 300, response_dog.text
    response_get = test_app.get(url)
    assert response_get.status_code == 200, response_get.text
    assert response_get.json()["id"] == data_dog["id"]
    assert response_get.json()["name"] == "Estrella"
    assert response_get.json()["in_charge_id"] == user_standard["id"]
    assert response_get.json()["owner_id"] == user_standard["id"]


def test_get_inexistent_dog_by_name(test_app: TestClient):
    url = endpoint+"/Estrella"
    response = test_app.get(url)
    assert response.status_code == 404, response.text
    assert response.json() == {"detail":"Dog not found"}


def test_delete_dog(test_app: TestClient):
    url = endpoint+"/Estrella"
    data_dog = {
        "id": 1,
        "owner_email": user_standard["email"]
    }
    response_create = create_user(test_app, "/api/v1/users", user_standard)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app, "/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    response_dog = create_dog(test_app, url, headers, data_dog)
    assert response_dog.status_code >= 200 and response_dog.status_code < 300, response_dog.text
    response_delete = test_app.delete(url, headers=headers)
    assert response_delete.status_code == 200


def test_delete_inexistent_dog(test_app: TestClient):
    url = endpoint+"/Estrella"
    response_create = create_user(test_app, "/api/v1/users", user_standard)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app, "/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    response_delete = test_app.delete(url, headers=headers)
    assert response_delete.status_code == 404
    assert response_delete.json() == {"detail":"Dog not found: There is not a dog with this name"}


@pytest.mark.parametrize("field_updated", [
    pytest.param(updates[0], marks=[pytest.mark.dependency(name="update_name")]),
    pytest.param(updates[1], marks=[pytest.mark.dependency(name="update_photo")]),
    pytest.param(updates[2], marks=[pytest.mark.dependency(name="update_name_photo")]),
])
def test_update_dog(test_app: TestClient, field_updated: dict):
    url = endpoint+"/Estrella"
    data_dog = {
        "id": 1,
        "owner_email": user_standard["email"]
    }
    response_create = create_user(test_app, "/api/v1/users", user_standard)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app, "/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    response_dog = create_dog(test_app, url, headers, data_dog)
    assert response_dog.status_code >= 200 and response_dog.status_code < 300, response_dog.text
    response_update = test_app.put(url, json=field_updated, headers=headers)
    assert response_update.status_code == 200, response_update.text


@pytest.mark.parametrize("field_updated", [
    pytest.param(updates[0], marks=[pytest.mark.dependency(name="update_name_inexistent")]),
    pytest.param(updates[1], marks=[pytest.mark.dependency(name="update_photo_inexistent")]),
    pytest.param(updates[2], marks=[pytest.mark.dependency(name="update_name_photo_inexistent")]),
])
def test_update_inexistent_dog(test_app: TestClient, field_updated: dict):
    url = endpoint+"/Estrella"
    data_dog = {
        "id": 1,
        "owner_email": user_standard["email"]
    }
    response_create = create_user(test_app, "/api/v1/users", user_standard)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user_standard["email"],
        "password": user_standard["password"]
    }
    response_login = authenticate(test_app, "/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    response_update = test_app.put(url, json=field_updated, headers=headers)
    assert response_update.status_code == 404, response_update.text
    assert response_update.json() == {"detail":"Dog not found: There is not a dog with this name"}


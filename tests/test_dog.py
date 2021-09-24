
from tests.utils import create_user, create_dog
from tests.test_login import authenticate


endpoint = "/api/v1/dogs"

def test_get_dogs_empty(test_app):
    url = endpoint
    response = test_app.get(url)
    assert response.status_code == 404
    assert response.json() == {"detail": "Dogs not found"}


def test_is_adopted(test_app):
    url = endpoint+"/is_adopted"
    user = {
        "id": 9,
        "name": "Laura",
        "last_name": "Ferandez",
        "email": "lau@mail.com",
        "password": "hola",
        "is_active": True,
    }
    response_create = create_user(test_app,"/api/v1/users", user)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user["email"],
        "password": user["password"]
    }
    data_dog = {
        "id": 1,
        "owner_email": user["email"]
    }
    response_login = authenticate(test_app,"/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    response_dog = create_dog(test_app, "/api/v1/dogs/Estrello", headers, data_dog)
    assert response_dog.status_code == 200, response_dog.text
    assert response_dog.json()["in_charge_id"] == user["id"]
    assert response_dog.json()["is_adopted"] == True
    response_adopted = test_app.get(url)
    assert response_adopted.status_code ==200
    assert isinstance(response_adopted.json(), list)
    assert isinstance(response_adopted.json()[0], dict)


def test_adopt(test_app):
    url = endpoint+"/adopt/Chispas"
    user = {
        "id": 10,
        "name": "Ruth",
        "last_name": "Montoya",
        "email": "ruth@mail.com",
        "password": "hola",
        "is_active": True,
    }
    response_create = create_user(test_app, "/api/v1/users", user)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user["email"],
        "password": user["password"]
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
    assert response_dog.json()["in_charge_id"] == user["id"]
    assert response_dog.json()["is_adopted"] == False
    response_adopt = test_app.put(f"{url}?owner_email={user['email']}", headers=headers)
    assert response_adopt.status_code == 200, response_adopt.text




def test_create_dog(test_app):
    url = endpoint+"/Estrella"
    user = {
        "id": 15,
        "name": "Julian",
        "last_name": "Gomez",
        "email": "jul@mail.com",
        "password": "hola",
        "is_active": True,
    }
    response_create = create_user(test_app, "/api/v1/users", user)
    assert response_create.status_code == 200, response_create.text
    data_login = {
        "username": user["email"],
        "password": user["password"]
    }
    data_dog = {
        "id": 5
    }
    response_login = authenticate(test_app, "/api/v1/login/token", data_login)
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()
    headers = {
        "Authorization": "Bearer "+token['access_token']
    }
    response_dog = create_dog(test_app, url, headers, data_dog)
    assert response_dog.status_code == 200, response_dog.text
    assert response_dog.json()["id"] == data_dog["id"]
    assert response_dog.json()["name"] == "Estrella"
    assert response_dog.json()["in_charge_id"] == user["id"]

    
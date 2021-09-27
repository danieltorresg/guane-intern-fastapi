import pytest
from starlette.testclient import TestClient

from app.core.security import verify_password

from tests.utils import create_user


endpoint = "/api/v1/users"

some_users = [{
        "id": 70,
        "name": "Daniel",
        "last_name": "Torres",
        "email": "mail1@mail.com",
        "password": "hola",
        "is_active": True,
    },
    {
        "id": 71,
        "name": "Daniel",
        "last_name": "Torres",
        "email": "mail2@mail.com",
        "password": "hola",
        "is_active": True,
    }
]

user_standard = {
    "id": 2,
    "name": "Daniel",
    "last_name": "Torres",
    "email": "daniel@mail.com",
    "password": "hola",
    "is_active": True,
}

user_same_id = {
    "id": 2,
    "name": "Daniel",
    "last_name": "Torres",
    "email": "daniel@mail.com",
    "password": "hola",
    "is_active": True,
}


user_same_email = {
    "id": 3,
    "name": "Daniel",
    "last_name": "Torres",
    "email": "dan@mail.com",
    "password": "hola",
    "is_active": True,
}

user_deactivate = {
    "id": 3,
    "name": "Daniel",
    "last_name": "Torres",
    "email": "dan@mail.com",
    "password": "hola",
    "is_active": False,

}

updates = [
    {
        "name": "Leidy"
    },
    {
        "last_name": "Gonzalez"
    },
    {
        "email": "leidy@mail.com"
    },
    {
        "password": "adios"
    }
]


"""" Es un 200 y retornar un arreglo vacio """
# def test_get_users_empty(test_app: TestClient):
#     url = endpoint
#     response = test_app.get(url)
#     assert response.status_code == 200
#     assert response.json() == []


# @pytest.mark.parametrize("some_users", [
#     pytest.param(some_users, marks=[pytest.mark.dependency(name="users_full")])
# ])
# def test_get_users_full(test_app: TestClient, some_users: list):
#     url = endpoint
#     for user in some_users:
#         response = create_user(test_app, endpoint, user)
#         assert response.status_code >= 200 and response.status_code < 300        
#     response = test_app.get(url) 
#     assert response.status_code == 200, response.text
#     assert isinstance(response.json(), list)
#     assert isinstance(response.json()[0], dict)


# def test_create_user(test_app: TestClient):
#     url = endpoint
#     data = user_standard
#     response = create_user(test_app, url, data)
#     assert response.status_code == 200
#     assert response.json()["id"]
#     assert response.json()["name"] == data["name"]
#     assert response.json()["last_name"] == data["last_name"]
#     assert response.json()["email"] == data["email"]
#     assert response.json()["is_active"] == data["is_active"]


# @pytest.mark.parametrize("duplicate_user", [
#     pytest.param(user_same_id, marks=[pytest.mark.dependency(name="duplicate_id")]),
#     pytest.param(user_same_email, marks=[pytest.mark.dependency(name="duplicate_email")]),
# ])
# def test_create_duplicate_user(test_app: TestClient, duplicate_user: dict):
#     url = endpoint
#     data = {
#         "id": 2,
#         "name": "Daniel",
#         "last_name": "Torres",
#         "email": "dan@mail.com",
#         "password": "hola",
#         "is_active": True,
#     }
#     response_user = create_user(test_app, url, data)
#     assert response_user.status_code == 200
#     response_duplicate = create_user (test_app, url, duplicate_user)
#     assert response_duplicate.status_code >= 400 and response_duplicate.status_code < 500, response_duplicate.text
#     assert response_duplicate.json() == {"detail": "Duplicate key: There is a user with tis data"}


# def test_get_uploadfile(test_app: TestClient):
#     url = endpoint+"/upload_file"
#     response = test_app.get(url)
#     assert response.status_code == 200
#     assert response.json() == {"filename": "guane_file.txt"}


# @pytest.mark.parametrize("user", [
#     pytest.param(user_standard, marks=[pytest.mark.dependency(name="deactivate_standard")]),
#     pytest.param(user_deactivate, marks=[pytest.mark.dependency(name="deactivate_userdeactivate")]),
# ])
# def test_deactivate_user(test_app: TestClient, user: dict):
#     url = endpoint+"/deactivate"
#     response_create = create_user(test_app, endpoint, user)
#     assert response_create.status_code == 200, response_create.text
#     response = test_app.put(url, params={"id":user["id"]})
#     assert response.status_code == 200, response.text
#     assert response.json()["is_active"] == False


# def test_deactivate_inexistent_user(test_app: TestClient):
#     url = endpoint+"/deactivate"
#     response = test_app.put(url, params={"id":2})
#     assert response.status_code == 404, response.text
#     assert response.json() == {"detail":"User not found: There is not a user with this id"}


# @pytest.mark.parametrize("user", [
#     pytest.param(user_standard, marks=[pytest.mark.dependency(name="get_by_id")]),
# ])
# def test_get_user_by_id(test_app: TestClient, user: dict):
#     url = endpoint+f"/{user['id']}"
#     response_create = create_user(test_app, endpoint, user)
#     assert response_create.status_code == 200, response_create.text
#     response = test_app.get(url)
#     assert response.status_code == 200, response.text
#     assert response.json()["id"] == user["id"]
#     assert response.json()["name"] == user["name"]
#     assert response.json()["last_name"] == user["last_name"]
#     assert response.json()["email"] == user["email"]
#     assert response.json()["is_active"] == True
#     assert response.json()["created_date"]


# def test_get_inexistent_user_by_id(test_app: TestClient):
#     url = endpoint+"1"
#     response = test_app.get(url)
#     assert response.status_code == 404, response.text
#     assert response.json() == {"detail":"Not Found"}


# @pytest.mark.parametrize("user, field_updated", [
#     pytest.param(user_standard, updates[0], marks=[pytest.mark.dependency(name="update_name")]),
#     pytest.param(user_standard, updates[1], marks=[pytest.mark.dependency(name="update_last_name")]),
#     pytest.param(user_standard, updates[2], marks=[pytest.mark.dependency(name="update_password")]),
# ])
# def test_update_user(test_app: TestClient, user: dict, field_updated: dict):
#     url = endpoint+f"/{user['id']}"
#     response_create = create_user(test_app, endpoint, user)
#     assert response_create.status_code == 200, response_create.text
#     response = test_app.put(url, json=field_updated)
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)


# @pytest.mark.parametrize("field_updated", [
#     pytest.param(updates[0], marks=[pytest.mark.dependency(name="update_name_inexistent")]),
#     pytest.param(updates[1], marks=[pytest.mark.dependency(name="update_last_name_inexistent")]),
#     pytest.param(updates[2], marks=[pytest.mark.dependency(name="update_password_inexistent")]),
# ])
# def test_update_inexistent_user(test_app: TestClient, field_updated: dict):
#     url = endpoint+"/1"
#     response = test_app.put(url, json=field_updated)
#     assert response.status_code == 404, response.text
#     assert response.json() == {"detail":"User not found: There is not a user with this id"}

# @pytest.mark.parametrize("user", [
#     pytest.param(user_standard, marks=[pytest.mark.dependency(name="delete_user")]),
# ])
# def test_delete_user(test_app: TestClient, user: dict):
#     url = endpoint+f"/{user['id']}"
#     response_create = create_user(test_app, endpoint, user)
#     assert response_create.status_code == 200, response_create.text
#     response = test_app.delete(url)
#     assert response.json()["id"] == user["id"]
#     assert response.json()["name"] == user["name"]
#     assert response.json()["last_name"] == user["last_name"]
#     assert response.json()["email"] == user["email"]
#     assert response.json()["is_active"] == True
#     assert response.json()["created_date"]
#     assert verify_password(user["password"],response.json()["password"])   


@pytest.mark.parametrize("some_users", [
    pytest.param(some_users, marks=[pytest.mark.dependency(name="filter_users_full")])
])
def test_filter_name_full(test_app: TestClient, some_users: list):
    url = endpoint + "/filter_by_name"
    for user in some_users:
        response_create = create_user(test_app, endpoint, user)
        assert response_create.status_code >= 200 and response_create.status_code < 300  
    response_filter = test_app.get(url, params={"name":"Daniel"})
    assert response_filter.status_code == 200, response_filter.text
    assert isinstance(response_filter.json(), list)
    assert isinstance(response_filter.json()[0], dict)
    for user in response_filter.json():
        assert user["name"] == "Daniel"


@pytest.mark.parametrize("some_users", [
    pytest.param(some_users, marks=[pytest.mark.dependency(name="filter_users_full_daniel")]),
    pytest.param([], marks=[pytest.mark.dependency(name="filter_users_empty")]),
])
def test_filter_name_empty(test_app: TestClient, some_users: list):
    url = endpoint + "/filter_by_name"
    for user in some_users:
        response_create = create_user(test_app, endpoint, user)
        assert response_create.status_code >= 200 and response_create.status_code < 300  
    response_filter = test_app.get(url, params={"name":"Leidy"})
    assert response_filter.status_code == 200, response_filter.text
    assert isinstance(response_filter.json(), list)
    assert response_filter.json() == []

    
    


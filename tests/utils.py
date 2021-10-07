from starlette.testclient import TestClient


def create_user(test_app: TestClient, enpoint: str, data: dict):
    response = test_app.post(enpoint, json=data)
    return response


def authenticate(test_app: TestClient, url, data):
    return test_app.post(url, data=data)


def create_dog(test_app: TestClient, url, headers, data_dog):
    response = test_app.post(url, headers=headers, json=data_dog)
    return response

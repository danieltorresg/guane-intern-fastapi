
from app.core.security import verify_password

def create_user(test_app, enpoint: str, data: dict):
    response = test_app.post(enpoint,json=data)
    return response


def authenticate(test_app, url, data):
    return test_app.post(url, data=data)


def create_dog(test_app, url, headers, data_dog):
    response = test_app.post(url, headers=headers, json=data_dog)
    return response
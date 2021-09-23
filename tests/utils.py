from fastapi.testclient import TestClient
from app.core.security import verify_password

from app.main import app

client = TestClient(app)

def create_user(enpoint: str, data: dict):
    response = client.post(enpoint,json=data)
    return response
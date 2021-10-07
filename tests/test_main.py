from fastapi.testclient import TestClient


def test_read_main(test_app: TestClient):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"detail": "index guane app"}

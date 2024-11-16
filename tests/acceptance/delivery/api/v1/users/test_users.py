from http.client import CREATED, OK

from expects import equal, expect
from fastapi.testclient import TestClient

from main import app


class TestUsers:
    def test_create_user(self) -> None:
        client = TestClient(app)
        name = "yes"
        age = 38
        payload = {"name": name, "age": age}

        response = client.post("/api/v1/users", json=payload)

        expect(response.status_code).to(equal(CREATED))

        user_id = response.json()["id"]

        response = client.get(f"/api/v1/users/{user_id}")

        expect(response.status_code).to(equal(OK))
        user = response.json()
        expect(user).to(equal({"id": user_id, "name": name, "age": age}))

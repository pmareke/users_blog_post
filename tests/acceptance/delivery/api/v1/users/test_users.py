from http.client import CREATED, INTERNAL_SERVER_ERROR, NOT_FOUND, OK

from doublex import ANY_ARG, Mimic, Stub
from expects import equal, expect
from fastapi.testclient import TestClient

from main import app
from src.delivery.api.v1.users.users_router import (
    _create_user_command_handler,
    _get_user_query_handler,
)
from src.domain.exceptions import CreateUserCommandException, GetUserQueryException
from src.use_cases.commands.create_user_command import CreateUserCommandHandler
from src.use_cases.queries.get_user_query_handler import GetUserQueryHandler


class TestUsers:
    def test_create_and_get_user(self) -> None:
        client = TestClient(app)
        name = "yes"
        age = 38
        payload = {"name": name, "age": age}

        response = client.post("/api/v1/users", json=payload)

        expect(response.status_code).to(equal(CREATED))

        user_id = response.json()["id"]
        response = client.get(f"/api/v1/users/{user_id}")

        user = response.json()
        expect(response.status_code).to(equal(OK))
        expect(user).to(equal({"id": user_id, "name": name, "age": age}))

    def test_user_not_found(self) -> None:
        id = 1
        client = TestClient(app)
        response = client.get(f"/api/v1/users/{id}")

        expect(response.status_code).to(equal(NOT_FOUND))
        expect(response.json()).to(equal({"detail": f"Item '{id}' not found"}))

    def test_internal_server_error_when_creating(self) -> None:
        payload = {"name": "yes", "age": 38}
        client = TestClient(app)

        def _handler() -> CreateUserCommandHandler:
            with Mimic(Stub, CreateUserCommandHandler) as handler:
                handler.execute(ANY_ARG).raises(CreateUserCommandException)
            return handler

        app.dependency_overrides[_create_user_command_handler] = _handler
        response = client.post(f"/api/v1/users", json=payload)

        expect(response.status_code).to(equal(INTERNAL_SERVER_ERROR))
        expect(response.json()).to(equal({"detail": "Sorry for the noise!"}))

    def test_internal_server_error_when_searching(self) -> None:
        id = 1
        client = TestClient(app)

        def _handler() -> GetUserQueryHandler:
            with Mimic(Stub, GetUserQueryHandler) as handler:
                handler.execute(ANY_ARG).raises(GetUserQueryException)
            return handler

        app.dependency_overrides[_get_user_query_handler] = _handler
        response = client.get(f"/api/v1/users/{id}")

        expect(response.status_code).to(equal(INTERNAL_SERVER_ERROR))
        expect(response.json()).to(equal({"detail": "Sorry for the noise!"}))

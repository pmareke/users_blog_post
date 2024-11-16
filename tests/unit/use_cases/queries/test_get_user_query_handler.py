from uuid import uuid4

from doublex import Mimic, Stub
from expects import equal, expect

from src.domain.users.user import User
from src.infrastructure.postgres.postgres_users_repository import (
    PostgresUsersRepository,
)
from src.use_cases.queries.get_user_query_handler import (
    GetUserQuery,
    GetUserQueryHandler,
)


class TestGetUserQueryHandler:
    def test_get_user(self) -> None:
        user_id = uuid4().hex
        expected_user = User(user_id=user_id, name="John Doe", age=20)
        with Mimic(Stub, PostgresUsersRepository) as repository:
            repository.get(user_id).returns(expected_user)
        query = GetUserQuery(user_id)
        handler = GetUserQueryHandler(repository)

        response = handler.execute(query)

        user = response.message()
        expect(user).to(equal(expected_user))

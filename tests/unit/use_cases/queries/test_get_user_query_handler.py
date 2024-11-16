from uuid import uuid4

from doublex import ANY_ARG, Mimic, Stub
from expects import expect, raise_error

from src.domain.exceptions import (
    GetUserQueryException,
    NotFoundUsersRepositoryException,
    UsersRepositoryException,
)
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

    def test_raise_exception_when_getting_a_user(self) -> None:
        with Mimic(Stub, PostgresUsersRepository) as repository:
            repository.get(ANY_ARG).raises(UsersRepositoryException)
        user_id = uuid4().hex
        command = GetUserQuery(user_id)
        handler = GetUserQueryHandler(repository)

        expect(lambda: handler.execute(command)).to(raise_error(GetUserQueryException))

    def test_raise_exception_when_getting_a_non_existing_user(self) -> None:
        with Mimic(Stub, PostgresUsersRepository) as repository:
            repository.get(ANY_ARG).raises(NotFoundUsersRepositoryException)
        user_id = uuid4().hex
        command = GetUserQuery(user_id)
        handler = GetUserQueryHandler(repository)

        expect(lambda: handler.execute(command)).to(raise_error(GetUserQueryException))

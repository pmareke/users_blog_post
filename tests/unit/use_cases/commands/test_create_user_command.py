from uuid import uuid4

from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect

from src.domain.users.user import User
from src.infrastructure.postgres.postgres_users_repository import (
    PostgresUsersRepository,
)
from src.use_cases.commands.create_user_command import (
    CreateUserCommand,
    CreateUserCommandHandler,
)


class TestCreateUserCommand:
    def test_create_user(self) -> None:
        repository = Mimic(Spy, PostgresUsersRepository)
        user_id = uuid4().hex
        name = "John Doe"
        age = 30
        user = User(user_id=user_id, name=name, age=age)
        command = CreateUserCommand(user)
        handler = CreateUserCommandHandler(repository)

        handler.execute(command)

        expect(repository.save).to(have_been_called_with(user))

from src.domain.command import Command, CommandHandler
from src.domain.exceptions import CreateUserCommandException, UsersRepositoryException
from src.domain.users.user import User
from src.domain.users.users_repository import UsersRepository


class CreateUserCommand(Command):
    def __init__(self, user: User) -> None:
        super().__init__()
        self.user = user


class CreateUserCommandResponse:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def message(self) -> str:
        return self.user_id


class CreateUserCommandHandler(CommandHandler):
    def __init__(self, repository: UsersRepository) -> None:
        self.repository = repository

    def execute(self, command: CreateUserCommand) -> CreateUserCommandResponse:
        try:
            self.repository.save(command.user)
            return CreateUserCommandResponse(user_id=command.user.user_id)
        except UsersRepositoryException as ex:
            raise CreateUserCommandException from ex

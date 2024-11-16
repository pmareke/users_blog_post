from http.client import CREATED
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.common.settings import settings
from src.delivery.api.v1.users.created_user_response import CreatedUserResponse
from src.delivery.api.v1.users.user_request import UserRequest
from src.delivery.api.v1.users.user_response import UserResponse
from src.domain.command import CommandHandler
from src.domain.query import QueryHandler
from src.domain.users.user import User
from src.domain.users.users_repository import UsersRepository
from src.infrastructure.postgres.postgres_users_repository import (
    PostgresUsersRepository,
)
from src.use_cases.commands.create_user_command import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from src.use_cases.queries.get_user_query_handler import (
    GetUserQuery,
    GetUserQueryHandler,
)

users_router: APIRouter = APIRouter()


async def _get_users_repository() -> UsersRepository:
    engine = create_engine(f"postgresql://{settings.db_dsn}")
    session = Session(engine)
    return PostgresUsersRepository(session)


async def _create_user_command_handler(
    repository: UsersRepository = Depends(_get_users_repository),
) -> CommandHandler:
    return CreateUserCommandHandler(repository)


async def _get_user_query_handler(
    repository: UsersRepository = Depends(_get_users_repository),
) -> QueryHandler:
    return GetUserQueryHandler(repository)


@users_router.post("/users", status_code=CREATED)
def _create(
    user_request: UserRequest,
    handler: CommandHandler = Depends(_create_user_command_handler),
) -> CreatedUserResponse:
    user_id = uuid4().hex
    name = user_request.name
    age = user_request.age
    user = User(user_id=user_id, name=name, age=age)
    command = CreateUserCommand(user)
    response = handler.execute(command)
    user_id = response.message()
    return CreatedUserResponse(id=user_id)


@users_router.get("/users/{id}", response_model=UserResponse)
def _get(
    id: str, handler: QueryHandler = Depends(_get_user_query_handler)
) -> UserResponse:
    command = GetUserQuery(id)
    response = handler.execute(command)
    user: User = response.message()
    return UserResponse(id=user.user_id, name=user.name, age=user.age)

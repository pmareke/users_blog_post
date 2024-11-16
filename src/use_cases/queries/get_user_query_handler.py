from src.domain.exceptions import (
    GetUserQueryException,
    NotFoundGetUserQueryException,
    NotFoundUsersRepositoryException,
    UsersRepositoryException,
)
from src.domain.query import Query, QueryHandler
from src.domain.users.user import User
from src.domain.users.users_repository import UsersRepository


class GetUserQuery(Query):
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id


class GetUserQueryResponse:
    def __init__(self, user: User) -> None:
        self.user = user

    def message(self) -> User:
        return self.user


class GetUserQueryHandler(QueryHandler):
    def __init__(self, repository: UsersRepository) -> None:
        self.repository = repository

    def execute(self, query: GetUserQuery) -> GetUserQueryResponse:
        try:
            user = self.repository.get(query.user_id)
            return GetUserQueryResponse(user)
        except UsersRepositoryException as ex:
            raise GetUserQueryException from ex
        except NotFoundUsersRepositoryException as ex:
            raise NotFoundGetUserQueryException from ex

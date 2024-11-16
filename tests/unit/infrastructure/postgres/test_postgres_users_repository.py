from doublex import ANY_ARG, Mimic, Spy
from doublex_expects import have_been_called
from expects import expect, raise_error
from sqlalchemy.orm import Session

from src.domain.exceptions import UsersRepositoryException
from src.domain.users.user import User
from src.infrastructure.postgres.postgres_users_repository import (
    PostgresUsersRepository,
)


class TestPostgresUsersRepository:
    def test_raise_exception_when_saving_a_user(self) -> None:
        user = User(user_id="test", name="test", age=18)
        with Mimic(Spy, Session) as session:
            session.add(ANY_ARG).raises(Exception)
        users_repository = PostgresUsersRepository(session)

        expect(lambda: users_repository.save(user)).to(
            raise_error(UsersRepositoryException)
        )
        expect(session.rollback).to(have_been_called)

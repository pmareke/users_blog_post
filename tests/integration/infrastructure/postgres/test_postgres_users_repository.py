from uuid import uuid4

import pytest
from expects import equal, expect, raise_error
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.common.settings import settings
from src.domain.exceptions import NotFoundUsersRepositoryException
from src.domain.users.user import User
from src.infrastructure.postgres.postgres_users_repository import (
    PostgresUsersRepository,
)


class TestPostgresUsersRepository:
    @pytest.fixture
    def session(self) -> Session:
        engine = create_engine(f"postgresql://{settings.db_dsn}")
        return Session(engine)

    def test_create_and_get_user(self, session: Session) -> None:
        user_id = uuid4().hex
        user = User(user_id=user_id, name="test", age=18)
        users_repository = PostgresUsersRepository(session)

        users_repository.save(user)
        found_user = users_repository.get(user_id)

        expect(found_user).to(equal(user))

    def test_raise_not_found_exceptions(self, session: Session) -> None:
        users_repository = PostgresUsersRepository(session)

        expect(lambda: users_repository.get("not_found")).to(
            raise_error(NotFoundUsersRepositoryException)
        )

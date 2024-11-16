from uuid import uuid4

from expects import equal, expect
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.common.settings import settings
from src.domain.users.user import User
from src.infrastructure.postgres.postgres_users_repository import (
    PostgresUsersRepository,
)


class TestPostgresUsersRepository:
    def test_create_and_get_user(self) -> None:
        engine = create_engine(f"postgresql://{settings.db_dsn}")
        session = Session(engine)
        user_id = uuid4().hex
        user = User(user_id=user_id, name="test", age=18)
        users_repository = PostgresUsersRepository(session)

        users_repository.save(user)
        found_user = users_repository.get(user_id)

        expect(found_user).to(equal(user))

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.domain.exceptions import (
    NotFoundUsersRepositoryException,
    UsersRepositoryException,
)
from src.domain.users.user import User
from src.domain.users.users_repository import UsersRepository


class PostgresUsersRepository(UsersRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, user: User) -> None:
        try:
            self.session.add(user)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise UsersRepositoryException from ex

    def get(self, id: str) -> User:
        try:
            stmt = select(User).where(User.user_id == id)
            return self.session.execute(stmt).scalar_one()
        except NoResultFound as ex:
            raise NotFoundUsersRepositoryException from ex

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.users.user import User
from src.domain.users.users_repository import UsersRepository


class PostgresUsersRepository(UsersRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()

    def get(self, id: UUID) -> User:
        stmt = select(User).where(User.user_id == id)
        return self.session.execute(stmt).scalar_one()

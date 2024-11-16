from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.users.user import User


class UsersRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: UUID) -> User:
        raise NotImplementedError

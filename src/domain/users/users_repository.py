from abc import ABC, abstractmethod

from src.domain.users.user import User


class UsersRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str) -> User:
        raise NotImplementedError

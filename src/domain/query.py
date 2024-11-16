import uuid
from abc import ABC, abstractmethod
from typing import Any


class Query:
    def __init__(self) -> None:
        self.query_id = uuid.uuid1()


class QueryResponse(ABC):
    @abstractmethod
    def message(self) -> Any:
        raise NotImplementedError()


class QueryHandler(ABC):
    @abstractmethod
    def execute(self, query: Query) -> QueryResponse:
        raise NotImplementedError()

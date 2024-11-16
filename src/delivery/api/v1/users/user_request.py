from dataclasses import dataclass


@dataclass
class UserRequest:
    name: str
    age: int

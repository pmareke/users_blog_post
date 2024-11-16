from datetime import datetime
from typing import Any

from sqlalchemy import Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.users.base import Base


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, autoincrement=False
    )
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Numeric)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __eq__(self, other: Any) -> bool:
        return bool(
            self.user_id == other.user_id
            and self.name == other.name
            and self.age == other.age
        )

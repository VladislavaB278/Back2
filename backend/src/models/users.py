from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base
from src.schemas.users import UserSchema


class Users(Base):
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            registered_at=self.registered_at,
            is_admin=self.is_admin,
        )

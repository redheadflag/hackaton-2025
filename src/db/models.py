from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from db.mixins import TimeStampedMixin


class User(TimeStampedMixin, Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)

    login: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(50), nullable=False)

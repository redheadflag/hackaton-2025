import uuid
from geoalchemy2 import Geometry
from sqlalchemy import UUID, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from db.base import Base
from db.enums import ChannelType
from db.mixins import DeletableMixin, TimeStampedMixin


class User(TimeStampedMixin, Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    login: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)

    channels: Mapped[list["Channel"]] = relationship(back_populates="creator", secondary="user_channels")


class Channel(TimeStampedMixin, DeletableMixin, Base):
    __tablename__ = "channels"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    creator_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    slug: Mapped[str] = mapped_column(String(50), nullable=False)

    type: Mapped[str] = mapped_column(Enum(ChannelType), nullable=False)

    creator: Mapped["User"] = relationship(back_populates="channels", secondary="user_channels", uselist=True)


class UserChannel(TimeStampedMixin, DeletableMixin, Base):
    __tablename__ = "user_channels"

    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), primary_key=True)
    channel_id: Mapped[str] = mapped_column(ForeignKey('channels.id'), primary_key=True)


class Message(TimeStampedMixin, DeletableMixin, Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id: Mapped[str] = mapped_column(ForeignKey("channels.id"), nullable=False)
    sender_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)

    content: Mapped[dict] = mapped_column(JSONB, nullable=False)

    point: Mapped[tuple[float, float]] = mapped_column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    
    title: Mapped[str] = mapped_column(String(50), nullable=True)

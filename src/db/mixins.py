from sqlalchemy import Boolean, Column, DateTime, func
from sqlalchemy.orm import declared_attr


class TimeStampedMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DeletableMixin:
    @declared_attr
    def is_deleted(cls):
        return Column(Boolean, default=False, nullable=False)

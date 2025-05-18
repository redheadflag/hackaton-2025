import logging
from typing import Any, Generic, Sequence, Type, TypeVar, Union
from pydantic import UUID4, BaseModel
from sqlalchemy import BinaryExpression, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base


ORMModel = TypeVar("ORMModel", bound=Base)

logger = logging.getLogger(__name__)


class NotFoundError(Exception):
    pass


class CRUDRepository(Generic[ORMModel]):
    def __init__(self, model: Type[ORMModel]) -> None:
        self._model = model

    async def create(self, session: AsyncSession, obj_schema: BaseModel) -> ORMModel:
        obj = self._model(**obj_schema.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def get(self, session: AsyncSession, pk: int | str | UUID4, *args, **kwargs) -> ORMModel | None:
        return await session.get(self._model, pk)

    async def update(self, session: AsyncSession, obj_id: int | str | UUID4, obj_updated: BaseModel) -> ORMModel:
        obj = await self.get(session, obj_id)
        if not obj:
            raise NotFoundError("Incorrect id provided")
        for key, value in obj_updated.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await session.commit()
        await session.refresh(obj)
        return obj
    
    async def filter(
        self,
        session: AsyncSession,
        *expressions: BinaryExpression,
    ) -> list[ORMModel]:
        stmt = select(self._model)
        if expressions:
            stmt = stmt.where(*expressions)
        return list(await session.scalars(stmt))

    async def delete(self, session: AsyncSession, obj_id: int | str | UUID4) -> None:
        obj = self.get(session, obj_id)
        if not obj:
            raise NotFoundError("Incorrect id provided")
        await session.delete(obj)
        await session.commit()

    async def get_all(self, session: AsyncSession, *args, **kwargs) -> Sequence[ORMModel]:
        return await self.filter(session=session)
    
    async def update_instance(self, session: AsyncSession, obj: ORMModel, **params) -> ORMModel:
        for key, value in params.items():
            setattr(obj, key, value)
        await session.commit()
        await session.refresh(obj)
        return obj
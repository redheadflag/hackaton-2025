from typing import AsyncGenerator

from db.base import sessionmaker


async def get_session() -> AsyncGenerator:
    async with sessionmaker() as session:
        yield session

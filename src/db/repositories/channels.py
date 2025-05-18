from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Channel
from db.repositories.crud import CRUDRepository
from schemas import ChannelCreate


class ChannelRepository(CRUDRepository):
    async def create(self, session: AsyncSession, channel_data: ChannelCreate, slug: str) -> Channel:
        channel = Channel(
            name = channel_data.name,
            type = channel_data.type,
            creator_id = channel_data.creator_id,
            slug=slug
        )
        session.add(channel)
        await session.commit()
        await session.refresh(channel)
        return channel


channel_repository = ChannelRepository(Channel)

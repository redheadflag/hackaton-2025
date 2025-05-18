from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from schemas import ChannelCreate, ChannelRead, ChannelBase
from db.repositories.channels import channel_repository

router = APIRouter(prefix="/channels")


@router.post("", response_model=ChannelRead, status_code=status.HTTP_201_CREATED)
async def create_channel(channel: ChannelCreate, session: AsyncSession = Depends(get_session)):
    return await channel_repository.create(session, channel)


@router.get("", response_model=list[ChannelRead])
async def list_channels(session: AsyncSession = Depends(get_session)):
    return await channel_repository.get_all(session)


@router.get("/{channel_id}", response_model=ChannelRead)
async def get_channel(channel_id: UUID4, session: AsyncSession = Depends(get_session)):
    channel = await channel_repository.get(session, channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel


@router.put("/{channel_id}", response_model=ChannelRead)
async def update_channel(channel_id: UUID4, channel: ChannelBase, session: AsyncSession = Depends(get_session)):
    # ChannelBase does not include creator_id, so only updatable fields
    return await channel_repository.update(session, channel_id, channel)


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(channel_id: UUID4, session: AsyncSession = Depends(get_session)):
    await channel_repository.delete(session, channel_id)
    return None


# The following endpoints would require a UserChannel repository and logic.
# Here are stubs for illustration; you should implement the repository and logic as needed.

@router.post("/{channel_id}/users")
async def add_user_to_channel(channel_id: UUID4, user: dict, session: AsyncSession = Depends(get_session)):
    # Implement logic to add a user to a channel (e.g., create UserChannel entry)
    return {"status": "user added to channel"}


@router.delete("/{channel_id}/users/{user_id}")
async def remove_user_from_channel(channel_id: UUID4, user_id: UUID4, session: AsyncSession = Depends(get_session)):
    # Implement logic to remove a user from a channel (e.g., delete UserChannel entry)
    return {"status": "user removed from channel"}
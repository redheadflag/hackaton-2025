import logging
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from schemas import MessageCreate, MessageRead
from db.repositories.messages import message_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/channels")


@router.post("/{channel_id}/messages", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def create_message(
    channel_id: UUID4,
    message: MessageCreate,
    session: AsyncSession = Depends(get_session)
):
    # Ensure the message is for the correct channel
    if message.channel_id != channel_id:
        raise HTTPException(status_code=400, detail="channel_id mismatch")
    return await message_repository.create(session, message)


@router.get("/{channel_id}/messages", response_model=list[MessageRead])
async def list_messages(
    channel_id: UUID4,
    sender_id: UUID4 | None = Query(None),
    
    session: AsyncSession = Depends(get_session)
):
    return await message_repository.get_all(session)

import logging
from typing import Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from geoalchemy2.shape import to_shape
from shapely import wkt
from db.models import Message
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
    lat, lon = message.point
    message.point = f"SRID=4326; POINT({lon} {lat})"

    # Ensure the message is for the correct channel
    if message.channel_id != channel_id:
        raise HTTPException(status_code=400, detail="channel_id mismatch")
    message_db = await message_repository.create(session, message)
    
    # Convert point back to tuple for response
    if hasattr(message_db, "point") and isinstance(message_db.point, str):
        # Remove SRID if present and parse WKT
        wkt_str = message_db.point.split(";", 1)[-1].strip()
        geom = wkt.loads(wkt_str)
        message_db.point = (geom.y, geom.x)
    
    message_out = MessageRead(
        channel_id=message_db.channel_id,
        sender_id=message_db.sender_id,
        content=message_db.content,
        point=(lat, lon),
        title=message_db.title,
        id=message_db.id
    )

    return message_out


@router.get("/{channel_id}/messages", response_model=list[MessageRead])
async def list_messages(
    channel_id: UUID4,
    sender_id: UUID4 | None = Query(None),
    session: AsyncSession = Depends(get_session)
):
    messages = await message_repository.filter(session, Message.channel_id==channel_id)

    messages_out = []
    for m in messages:
        point = None
        if hasattr(m, "point") and m.point is not None:
            try:
                # Convert WKBElement to shapely geometry
                geom = to_shape(m.point)
                point = (geom.y, geom.x)
            except Exception as e:
                logger.warning(f"Invalid point geometry: {m.point} ({e})")
        if point is None:
            continue

        messages_out.append(
            MessageRead(
                channel_id=m.channel_id,
                sender_id=m.sender_id,
                content=m.content,
                point=point,
                title=m.title,
                id=m.id
            )
        )
    return messages_out

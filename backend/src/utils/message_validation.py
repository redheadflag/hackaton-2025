from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from db.enums import UserType
from db.models import User
from sqlalchemy import select

async def validate_message(session: AsyncSession, sender_id: UUID4) -> bool:
    # Fetch sender
    sender = await session.get(User, sender_id)
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")

    # If robot, accept automatically
    if sender.user_type == UserType.ROBOT:
        return True

    # If human, check with oracles
    # (Not implemented so far hence just remove True)
    return True

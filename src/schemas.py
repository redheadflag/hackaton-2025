from pydantic import BaseModel, UUID4
from typing import Optional, Tuple
# from uuid import UUID

from db.enums import ChannelType, UserType

# User Schemas
class UserBase(BaseModel):
    login: str
    is_oracle: bool = False
    user_type: UserType = UserType.HUMAN


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    pass

class UserRead(UserBase):
    id: UUID4

    class Config:
        from_attributes = True


# Channel Schemas
class ChannelBase(BaseModel):
    name: str
    type: ChannelType


class ChannelCreate(ChannelBase):
    creator_id: UUID4


class ChannelRead(ChannelBase):
    id: UUID4
    slug: str
    creator_id: UUID4

    class Config:
        from_attributes = True


# UserChannel Schemas
class UserChannelBase(BaseModel):
    user_id: UUID4
    channel_id: UUID4


class UserChannelCreate(UserChannelBase):
    pass


class UserChannelRead(UserChannelBase):
    class Config:
        from_attributes = True


# Message Schemas
class MessageBase(BaseModel):
    channel_id: UUID4
    sender_id: UUID4
    content: dict
    point: Tuple[float, float] | str
    title: Optional[str] = None


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: UUID4

    class Config:
        from_attributes = True

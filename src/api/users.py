from fastapi import APIRouter, Depends
from fastapi import status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from schemas import UserCreate, UserRead, UserUpdate
from db.repositories.users import user_repository


router = APIRouter(prefix="/users")


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_handler(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await user_repository.create(session, user)


@router.put("/{user_id}", response_model=UserRead)
async def update_user_handler(user_id: UUID4, user: UserUpdate, session: AsyncSession = Depends(get_session)):
    return await user_repository.update(session, user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_handler(user_id: UUID4, session: AsyncSession = Depends(get_session)):
    await user_repository.delete(session, user_id)
    return None

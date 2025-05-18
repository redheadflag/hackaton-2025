from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from db.repositories.crud import CRUDRepository
from schemas import UserCreate


class UserRepository(CRUDRepository):
    async def create(self, session: AsyncSession, user_schema: UserCreate):
        obj = User(
            login=user_schema.login,
            password_hash=user_schema.password_hash
        )
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj



user_repository = UserRepository(User)

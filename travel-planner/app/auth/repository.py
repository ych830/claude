from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.model import User


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: str) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_oauth(self, provider: str, oauth_id: str) -> User | None:
        result = await self.db.execute(
            select(User).where(
                User.oauth_provider == provider,
                User.oauth_id == oauth_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, email: str, hashed_password: str | None, name: str | None,
                     oauth_provider: str | None = None, oauth_id: str | None = None,
                     profile_image: str | None = None) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
            name=name,
            oauth_provider=oauth_provider,
            oauth_id=oauth_id,
            profile_image=profile_image,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model import UserPreference, TravelHistory


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_preference(self, user_id: str) -> UserPreference | None:
        result = await self.db.execute(
            select(UserPreference).where(UserPreference.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def upsert_preference(self, user_id: str, **kwargs) -> UserPreference:
        pref = await self.get_preference(user_id)
        if pref:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(pref, key, value)
        else:
            pref = UserPreference(user_id=user_id, **{k: v for k, v in kwargs.items() if v is not None})
            self.db.add(pref)
        await self.db.flush()
        await self.db.refresh(pref)
        return pref

    async def get_travel_histories(self, user_id: str) -> list[TravelHistory]:
        result = await self.db.execute(
            select(TravelHistory)
            .where(TravelHistory.user_id == user_id)
            .order_by(TravelHistory.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_travel_history(self, user_id: str, destination: str,
                                     travel_date=None, memo: str | None = None) -> TravelHistory:
        history = TravelHistory(
            user_id=user_id,
            destination=destination,
            travel_date=travel_date,
            memo=memo,
        )
        self.db.add(history)
        await self.db.flush()
        await self.db.refresh(history)
        return history

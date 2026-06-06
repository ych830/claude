from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.model import User
from app.users.repository import UserRepository
from app.users.schema import PreferenceUpdate, TravelHistoryCreate


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def get_my_profile(self, user: User) -> dict:
        pref = await self.repo.get_preference(user.id)
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "profile_image": user.profile_image,
            "preference": pref,
        }

    async def update_preferences(self, user: User, data: PreferenceUpdate) -> dict:
        pref = await self.repo.upsert_preference(
            user.id,
            gender=data.gender,
            age=data.age,
            companion_type=data.companion_type,
            travel_styles=data.travel_styles,
            budget_range=data.budget_range,
            transport_pref=data.transport_pref,
        )
        return {
            "gender": pref.gender,
            "age": pref.age,
            "companion_type": pref.companion_type,
            "travel_styles": pref.travel_styles,
            "budget_range": pref.budget_range,
            "transport_pref": pref.transport_pref,
        }

    async def get_travel_histories(self, user: User) -> list:
        histories = await self.repo.get_travel_histories(user.id)
        return [
            {"id": h.id, "destination": h.destination,
             "travel_date": str(h.travel_date) if h.travel_date else None,
             "memo": h.memo}
            for h in histories
        ]

    async def add_travel_history(self, user: User, data: TravelHistoryCreate) -> dict:
        history = await self.repo.create_travel_history(
            user.id, data.destination, data.travel_date, data.memo
        )
        return {
            "id": history.id,
            "destination": history.destination,
            "travel_date": str(history.travel_date) if history.travel_date else None,
            "memo": history.memo,
        }

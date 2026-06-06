from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.model import User
from app.common.response import ok
from app.core.database import get_db
from app.users.schema import PreferenceUpdate, TravelHistoryCreate
from app.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    profile = await service.get_my_profile(current_user)
    return ok(profile)


@router.put("/me/preferences")
async def update_preferences(
    body: PreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    pref = await service.update_preferences(current_user, body)
    return ok(pref, "취향이 업데이트되었습니다.")


@router.get("/me/travel-history")
async def get_travel_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    histories = await service.get_travel_histories(current_user)
    return ok(histories)


@router.post("/me/travel-history")
async def add_travel_history(
    body: TravelHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    history = await service.add_travel_history(current_user, body)
    return ok(history, "여행 이력이 추가되었습니다.")

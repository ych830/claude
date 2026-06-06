from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import ok
from app.core.database import get_db
from app.places.schema import PlaceResponse
from app.places.service import PlaceService

router = APIRouter(prefix="/places", tags=["Places"])


@router.get("/search")
async def search_places(
    q: str = Query(..., min_length=1, description="검색어"),
    provider: Literal["google", "kakao"] = Query("kakao", description="지도 제공자"),
    lat: float | None = Query(None, description="검색 기준 위도"),
    lng: float | None = Query(None, description="검색 기준 경도"),
    db: AsyncSession = Depends(get_db),
):
    service = PlaceService(db)
    places = await service.search(q, provider=provider, lat=lat, lng=lng)
    return ok([PlaceResponse.model_validate(p).model_dump() for p in places])


@router.get("/{place_id}")
async def get_place(place_id: str, db: AsyncSession = Depends(get_db)):
    service = PlaceService(db)
    place = await service.get_detail(place_id)
    return ok(PlaceResponse.model_validate(place).model_dump())


@router.get("/{place_id}/nearby")
async def get_nearby_places(
    place_id: str,
    category: str | None = Query(None, description="카테고리 (restaurant, cafe, attraction 등)"),
    provider: Literal["google", "kakao"] = Query("kakao"),
    radius: int = Query(1000, ge=100, le=5000, description="반경(미터)"),
    db: AsyncSession = Depends(get_db),
):
    service = PlaceService(db)
    places = await service.get_nearby(place_id, category=category, provider=provider, radius=radius)
    return ok([PlaceResponse.model_validate(p).model_dump() for p in places])

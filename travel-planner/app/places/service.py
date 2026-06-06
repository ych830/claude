from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.google_maps_client import GoogleMapsClient
from app.clients.kakao_map_client import KakaoMapClient
from app.core.exceptions import NotFoundException
from app.places.model import Place
from app.places.repository import PlaceRepository


class PlaceService:
    def __init__(self, db: AsyncSession):
        self.repo = PlaceRepository(db)
        self.google = GoogleMapsClient()
        self.kakao = KakaoMapClient()

    async def search(
        self,
        query: str,
        provider: str = "kakao",
        lat: float | None = None,
        lng: float | None = None,
    ) -> list[Place]:
        if provider == "google":
            results = await self.google.search_places(query)
        else:
            results = await self.kakao.search_places(query, x=lng, y=lat)

        places = []
        for r in results:
            place = await self.repo.upsert_from_result(r)
            places.append(place)
        return places

    async def get_detail(self, place_id: str) -> Place:
        place = await self.repo.get_by_id(place_id)
        if not place:
            raise NotFoundException("장소를 찾을 수 없습니다.")
        return place

    async def get_nearby(
        self,
        place_id: str,
        category: str | None = None,
        provider: str = "kakao",
        radius: int = 1000,
    ) -> list[Place]:
        place = await self.repo.get_by_id(place_id)
        if not place:
            raise NotFoundException("장소를 찾을 수 없습니다.")

        if provider == "google":
            results = await self.google.search_nearby(
                place.latitude, place.longitude, radius=radius, category=category
            )
        else:
            results = await self.kakao.search_nearby(
                place.latitude, place.longitude, radius=radius, category=category
            )

        places = []
        for r in results:
            p = await self.repo.upsert_from_result(r)
            places.append(p)
        return places

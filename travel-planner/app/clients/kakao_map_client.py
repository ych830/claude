import httpx

from app.clients.map_types import PlaceResult
from app.core.config import settings
from app.core.exceptions import ExternalAPIException

_BASE = "https://dapi.kakao.com/v2/local"

# 카카오 카테고리 그룹 코드
_CATEGORY_CODE_MAP = {
    "restaurant": "FD6",
    "cafe": "CE7",
    "accommodation": "AD5",
    "shopping": "MT1",
    "attraction": "AT4",
    "cultural": "CT1",
    "transport": "SW8",
    "pharmacy": "PM9",
}


def _parse_document(doc: dict) -> PlaceResult:
    try:
        lat = float(doc.get("y", 0))
        lng = float(doc.get("x", 0))
    except (TypeError, ValueError):
        lat, lng = 0.0, 0.0

    return PlaceResult(
        external_id=str(doc.get("id", "")),
        name=doc.get("place_name", ""),
        latitude=lat,
        longitude=lng,
        source="kakao",
        category=doc.get("category_group_name") or doc.get("category_name", "").split(" > ")[-1],
        address=doc.get("road_address_name") or doc.get("address_name"),
        phone=doc.get("phone") or None,
        opening_hours=None,  # 카카오 기본 검색 API는 운영시간 미제공
        ticket_price=None,
        rating=None,
        image_url=None,
    )


class KakaoMapClient:
    def __init__(self):
        self._key = settings.kakao_rest_api_key

    def _headers(self) -> dict:
        return {"Authorization": f"KakaoAK {self._key}"}

    async def search_places(
        self, query: str, x: float | None = None, y: float | None = None
    ) -> list[PlaceResult]:
        params: dict = {"query": query, "size": 15}
        if x is not None and y is not None:
            params["x"] = x
            params["y"] = y

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(
                    f"{_BASE}/search/keyword.json",
                    params=params,
                    headers=self._headers(),
                )
                res.raise_for_status()
                data = res.json()
        except httpx.HTTPError as exc:
            raise ExternalAPIException("Kakao 장소 검색 중 오류가 발생했습니다.") from exc

        return [_parse_document(doc) for doc in data.get("documents", [])]

    async def search_nearby(
        self, lat: float, lng: float, radius: int = 1000, category: str | None = None
    ) -> list[PlaceResult]:
        category_code = _CATEGORY_CODE_MAP.get(category, "") if category else ""

        if category_code:
            params: dict = {
                "category_group_code": category_code,
                "x": lng,
                "y": lat,
                "radius": radius,
                "size": 15,
            }
            endpoint = f"{_BASE}/search/category.json"
        else:
            # 카테고리 없으면 좌표 기반 키워드 검색으로 fallback
            params = {"query": "관광명소", "x": lng, "y": lat, "radius": radius, "size": 15}
            endpoint = f"{_BASE}/search/keyword.json"

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(endpoint, params=params, headers=self._headers())
                res.raise_for_status()
                data = res.json()
        except httpx.HTTPError as exc:
            raise ExternalAPIException("Kakao 주변 검색 중 오류가 발생했습니다.") from exc

        return [_parse_document(doc) for doc in data.get("documents", [])]

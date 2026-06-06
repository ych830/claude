import httpx

from app.clients.map_types import PlaceResult
from app.core.config import settings
from app.core.exceptions import ExternalAPIException

_BASE = "https://maps.googleapis.com/maps/api"

_TYPE_MAP = {
    "restaurant": "restaurant",
    "cafe": "cafe",
    "accommodation": "lodging",
    "shopping": "shopping_mall",
    "attraction": "tourist_attraction",
    "cultural": "museum",
}


def _parse_place(raw: dict) -> PlaceResult:
    loc = raw.get("geometry", {}).get("location", {})
    types = raw.get("types", [])
    category = types[0] if types else None
    hours = raw.get("opening_hours")
    return PlaceResult(
        external_id=raw["place_id"],
        name=raw.get("name", ""),
        latitude=loc.get("lat", 0.0),
        longitude=loc.get("lng", 0.0),
        source="google",
        category=category,
        address=raw.get("formatted_address") or raw.get("vicinity"),
        phone=raw.get("formatted_phone_number"),
        opening_hours={"weekday_text": hours.get("weekday_text", [])} if hours else None,
        rating=raw.get("rating"),
        image_url=None,
    )


class GoogleMapsClient:
    def __init__(self):
        self._key = settings.google_maps_api_key

    async def search_places(self, query: str) -> list[PlaceResult]:
        params = {"query": query, "key": self._key, "language": "ko"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(f"{_BASE}/place/textsearch/json", params=params)
                res.raise_for_status()
                data = res.json()
        except httpx.HTTPError as exc:
            raise ExternalAPIException("Google Maps 검색 중 오류가 발생했습니다.") from exc

        if data.get("status") not in ("OK", "ZERO_RESULTS"):
            raise ExternalAPIException("Google Maps API 오류: " + data.get("status", ""))

        return [_parse_place(r) for r in data.get("results", [])]

    async def get_place_details(self, place_id: str) -> PlaceResult | None:
        fields = "place_id,name,formatted_address,geometry,formatted_phone_number,opening_hours,types,rating"
        params = {"place_id": place_id, "fields": fields, "key": self._key, "language": "ko"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(f"{_BASE}/place/details/json", params=params)
                res.raise_for_status()
                data = res.json()
        except httpx.HTTPError as exc:
            raise ExternalAPIException("Google Maps 상세 조회 중 오류가 발생했습니다.") from exc

        if data.get("status") != "OK":
            return None
        return _parse_place(data["result"])

    async def search_nearby(
        self, lat: float, lng: float, radius: int = 1000, category: str | None = None
    ) -> list[PlaceResult]:
        params: dict = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "key": self._key,
            "language": "ko",
        }
        if category:
            params["type"] = _TYPE_MAP.get(category, category)

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(f"{_BASE}/place/nearbysearch/json", params=params)
                res.raise_for_status()
                data = res.json()
        except httpx.HTTPError as exc:
            raise ExternalAPIException("Google Maps 주변 검색 중 오류가 발생했습니다.") from exc

        if data.get("status") not in ("OK", "ZERO_RESULTS"):
            raise ExternalAPIException("Google Maps API 오류: " + data.get("status", ""))

        return [_parse_place(r) for r in data.get("results", [])]

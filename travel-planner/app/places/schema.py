from typing import Literal

from pydantic import BaseModel


class PlaceResponse(BaseModel):
    id: str
    external_id: str
    name: str
    category: str | None
    address: str | None
    latitude: float
    longitude: float
    opening_hours: dict | None
    ticket_price: dict | None
    source: str
    phone: str | None
    rating: float | None
    image_url: str | None

    model_config = {"from_attributes": True}


class PlaceSearchParams(BaseModel):
    q: str
    provider: Literal["google", "kakao"] = "kakao"
    lat: float | None = None
    lng: float | None = None


class NearbySearchParams(BaseModel):
    category: str | None = None
    provider: Literal["google", "kakao"] = "kakao"
    radius: int = 1000

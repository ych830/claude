from dataclasses import dataclass, field


@dataclass
class PlaceResult:
    """Google/Kakao 검색 결과를 통일된 형태로 표현하는 공통 타입."""
    external_id: str
    name: str
    latitude: float
    longitude: float
    source: str                          # "google" | "kakao"
    category: str | None = None
    address: str | None = None
    phone: str | None = None
    opening_hours: dict | None = None
    ticket_price: dict | None = None
    rating: float | None = None
    image_url: str | None = None

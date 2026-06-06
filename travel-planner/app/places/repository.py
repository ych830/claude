from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.map_types import PlaceResult
from app.places.model import Place


class PlaceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, place_id: str) -> Place | None:
        result = await self.db.execute(select(Place).where(Place.id == place_id))
        return result.scalar_one_or_none()

    async def get_by_external_id(self, source: str, external_id: str) -> Place | None:
        result = await self.db.execute(
            select(Place).where(Place.source == source, Place.external_id == external_id)
        )
        return result.scalar_one_or_none()

    async def upsert_from_result(self, r: PlaceResult) -> Place:
        """외부 API 결과를 DB에 저장하거나 업데이트한다."""
        place = await self.get_by_external_id(r.source, r.external_id)
        if place:
            place.name = r.name
            place.category = r.category
            place.address = r.address
            place.latitude = r.latitude
            place.longitude = r.longitude
            if r.opening_hours:
                place.opening_hours = r.opening_hours
            if r.phone:
                place.phone = r.phone
            if r.rating is not None:
                place.rating = r.rating
        else:
            place = Place(
                external_id=r.external_id,
                name=r.name,
                category=r.category,
                address=r.address,
                latitude=r.latitude,
                longitude=r.longitude,
                opening_hours=r.opening_hours,
                ticket_price=r.ticket_price,
                source=r.source,
                phone=r.phone,
                rating=r.rating,
                image_url=r.image_url,
            )
            self.db.add(place)

        await self.db.flush()
        await self.db.refresh(place)
        return place

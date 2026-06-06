from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class PreferenceUpdate(BaseModel):
    gender: Literal["male", "female", "other"] | None = None
    age: int | None = Field(None, ge=1, le=120)
    companion_type: Literal["solo", "friend", "couple", "family", "group"] | None = None
    travel_purposes: list[str] | None = None
    budget_level: Literal["low", "mid", "high"] | None = None
    preferred_transport: list[str] | None = None
    disliked_categories: list[str] | None = None


class PreferenceResponse(BaseModel):
    gender: str | None
    age: int | None
    companion_type: str | None
    travel_purposes: list[str] | None
    budget_level: str | None
    preferred_transport: list[str] | None
    disliked_categories: list[str] | None

    model_config = {"from_attributes": True}


class TravelHistoryCreate(BaseModel):
    destination: str = Field(min_length=1, max_length=100)
    travel_date: date | None = None
    memo: str | None = None


class TravelHistoryResponse(BaseModel):
    id: str
    destination: str
    travel_date: date | None
    memo: str | None

    model_config = {"from_attributes": True}


class UserProfileResponse(BaseModel):
    id: str
    email: str
    name: str | None
    profile_image: str | None
    preference: PreferenceResponse | None = None

    model_config = {"from_attributes": True}

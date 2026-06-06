import uuid
from datetime import datetime

from sqlalchemy import String, Integer, DateTime, func, ForeignKey, Date
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), unique=True, nullable=False)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    companion_type: Mapped[str | None] = mapped_column(String, nullable=True)
    travel_styles: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    budget_range: Mapped[str | None] = mapped_column(String, nullable=True)
    transport_pref: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class TravelHistory(Base):
    __tablename__ = "travel_histories"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    destination: Mapped[str] = mapped_column(String, nullable=False)
    travel_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    memo: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

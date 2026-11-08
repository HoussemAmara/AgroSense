from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    gardens: Mapped[list["Garden"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )


class Garden(Base):
    __tablename__ = "gardens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    timezone: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner: Mapped["User"] = relationship(back_populates="gardens")
    plants: Mapped[list["Plant"]] = relationship(
        back_populates="garden", cascade="all, delete-orphan"
    )


class Species(Base):
    __tablename__ = "species"

    id: Mapped[int] = mapped_column(primary_key=True)
    perenual_id: Mapped[int | None] = mapped_column(unique=True)
    common_name: Mapped[str] = mapped_column(String(200), index=True)
    scientific_name: Mapped[str | None] = mapped_column(String(200))
    watering_category: Mapped[str | None] = mapped_column(String(50))
    sunlight: Mapped[list | None] = mapped_column(JSONB)
    image_url: Mapped[str | None] = mapped_column(String(500))
    moisture_min_pct: Mapped[float | None] = mapped_column(Float)
    moisture_max_pct: Mapped[float | None] = mapped_column(Float)
    moisture_source: Mapped[str] = mapped_column(
        String(30), default="default_mapping"
    )
    raw: Mapped[dict | None] = mapped_column(JSONB)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    plants: Mapped[list["Plant"]] = relationship(back_populates="species")


class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(primary_key=True)
    garden_id: Mapped[int] = mapped_column(
        ForeignKey("gardens.id", ondelete="CASCADE")
    )
    species_id: Mapped[int | None] = mapped_column(
        ForeignKey("species.id", ondelete="SET NULL")
    )
    nickname: Mapped[str] = mapped_column(String(100))
    planted_on: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)
    moisture_min_override: Mapped[float | None] = mapped_column(Float)
    moisture_max_override: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    garden: Mapped["Garden"] = relationship(back_populates="plants")
    species: Mapped["Species | None"] = relationship(back_populates="plants")
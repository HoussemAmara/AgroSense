from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
    model_validator,
)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GardenCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    timezone: str | None = Field(default=None, max_length=64)


class GardenUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    timezone: str | None = Field(default=None, max_length=64)


class GardenRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    latitude: float | None
    longitude: float | None
    timezone: str | None
    created_at: datetime

class SpeciesRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    common_name: str
    scientific_name: str | None
    watering_category: str | None
    sunlight: list[str] | None
    image_url: str | None
    moisture_min_pct: float | None
    moisture_max_pct: float | None
    moisture_source: str


def _check_range(lo: float | None, hi: float | None) -> None:
    if lo is not None and hi is not None and lo >= hi:
        raise ValueError("minimum moisture must be lower than maximum moisture")


class PlantCreate(BaseModel):
    nickname: str = Field(min_length=1, max_length=100)
    species_id: int | None = None
    planted_on: date | None = None
    notes: str | None = Field(default=None, max_length=2000)
    moisture_min_override: float | None = Field(default=None, ge=0, le=100)
    moisture_max_override: float | None = Field(default=None, ge=0, le=100)

    @model_validator(mode="after")
    def check_range(self):
        _check_range(self.moisture_min_override, self.moisture_max_override)
        return self


class PlantUpdate(BaseModel):
    nickname: str | None = Field(default=None, min_length=1, max_length=100)
    species_id: int | None = None
    planted_on: date | None = None
    notes: str | None = Field(default=None, max_length=2000)
    moisture_min_override: float | None = Field(default=None, ge=0, le=100)
    moisture_max_override: float | None = Field(default=None, ge=0, le=100)

    @model_validator(mode="after")
    def check_range(self):
        _check_range(self.moisture_min_override, self.moisture_max_override)
        return self


class PlantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    garden_id: int
    nickname: str
    planted_on: date | None
    notes: str | None
    species: SpeciesRead | None
    moisture_min_override: float | None
    moisture_max_override: float | None
    created_at: datetime

    @computed_field
    @property
    def target_moisture_min(self) -> float | None:
        if self.moisture_min_override is not None:
            return self.moisture_min_override
        return self.species.moisture_min_pct if self.species else None

    @computed_field
    @property
    def target_moisture_max(self) -> float | None:
        if self.moisture_max_override is not None:
            return self.moisture_max_override
        return self.species.moisture_max_pct if self.species else None
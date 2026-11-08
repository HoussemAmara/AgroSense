from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.deps import CurrentUser, DbSession
from app.models import Garden, Plant, Species
from app.routers.gardens import get_owned_garden
from app.schemas import PlantCreate, PlantRead, PlantUpdate

router = APIRouter(tags=["plants"])


def get_owned_plant(db: DbSession, user: CurrentUser, plant_id: int) -> Plant:
    plant = db.scalar(
        select(Plant)
        .join(Garden)
        .where(Plant.id == plant_id, Garden.user_id == user.id)
        .options(joinedload(Plant.species))
    )
    if plant is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Plant not found")
    return plant


def check_species(db: DbSession, species_id: int | None) -> None:
    if species_id is not None and db.get(Species, species_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Species not found")


@router.post(
    "/gardens/{garden_id}/plants",
    response_model=PlantRead,
    status_code=status.HTTP_201_CREATED,
)
def create_plant(
    garden_id: int, data: PlantCreate, db: DbSession, user: CurrentUser
):
    garden = get_owned_garden(db, user, garden_id)
    check_species(db, data.species_id)
    plant = Plant(garden_id=garden.id, **data.model_dump())
    db.add(plant)
    db.commit()
    return get_owned_plant(db, user, plant.id)


@router.get("/gardens/{garden_id}/plants", response_model=list[PlantRead])
def list_plants(garden_id: int, db: DbSession, user: CurrentUser):
    garden = get_owned_garden(db, user, garden_id)
    stmt = (
        select(Plant)
        .where(Plant.garden_id == garden.id)
        .options(joinedload(Plant.species))
        .order_by(Plant.created_at)
    )
    return db.scalars(stmt).unique().all()


@router.get("/plants/{plant_id}", response_model=PlantRead)
def get_plant(plant_id: int, db: DbSession, user: CurrentUser):
    return get_owned_plant(db, user, plant_id)


@router.patch("/plants/{plant_id}", response_model=PlantRead)
def update_plant(
    plant_id: int, data: PlantUpdate, db: DbSession, user: CurrentUser
):
    plant = get_owned_plant(db, user, plant_id)
    changes = data.model_dump(exclude_unset=True)
    if "species_id" in changes:
        check_species(db, changes["species_id"])
    for key, value in changes.items():
        if key == "nickname" and value is None:
            continue  # the nickname is required, it can't be emptied
        setattr(plant, key, value)
    db.commit()
    return get_owned_plant(db, user, plant_id)


@router.delete("/plants/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant(plant_id: int, db: DbSession, user: CurrentUser):
    plant = get_owned_plant(db, user, plant_id)
    db.delete(plant)
    db.commit()
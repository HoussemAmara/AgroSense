from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.deps import CurrentUser, DbSession
from app.models import Garden
from app.schemas import GardenCreate, GardenRead, GardenUpdate

router = APIRouter(prefix="/gardens", tags=["gardens"])


def get_owned_garden(db: DbSession, user: CurrentUser, garden_id: int) -> Garden:
    garden = db.scalar(
        select(Garden).where(Garden.id == garden_id, Garden.user_id == user.id)
    )
    if garden is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Garden not found")
    return garden


@router.post("", response_model=GardenRead, status_code=status.HTTP_201_CREATED)
def create_garden(data: GardenCreate, db: DbSession, user: CurrentUser):
    garden = Garden(user_id=user.id, **data.model_dump())
    db.add(garden)
    db.commit()
    db.refresh(garden)
    return garden


@router.get("", response_model=list[GardenRead])
def list_gardens(db: DbSession, user: CurrentUser):
    stmt = select(Garden).where(Garden.user_id == user.id).order_by(Garden.created_at)
    return db.scalars(stmt).all()


@router.get("/{garden_id}", response_model=GardenRead)
def get_garden(garden_id: int, db: DbSession, user: CurrentUser):
    return get_owned_garden(db, user, garden_id)


@router.patch("/{garden_id}", response_model=GardenRead)
def update_garden(
    garden_id: int, data: GardenUpdate, db: DbSession, user: CurrentUser
):
    garden = get_owned_garden(db, user, garden_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        if key == "name" and value is None:
            continue  # the name is required, it can't be emptied
        setattr(garden, key, value)
    db.commit()
    db.refresh(garden)
    return garden


@router.delete("/{garden_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_garden(garden_id: int, db: DbSession, user: CurrentUser):
    garden = get_owned_garden(db, user, garden_id)
    db.delete(garden)
    db.commit()
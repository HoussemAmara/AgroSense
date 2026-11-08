from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import or_, select

from app.deps import CurrentUser, DbSession
from app.models import Species
from app.schemas import SpeciesRead

router = APIRouter(prefix="/species", tags=["species"])


@router.get("", response_model=list[SpeciesRead])
def search_species(
    db: DbSession,
    user: CurrentUser,
    q: str | None = Query(default=None, max_length=100),
    limit: int = Query(default=20, ge=1, le=50),
):
    stmt = select(Species).order_by(Species.common_name).limit(limit)
    if q:
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(
                Species.common_name.ilike(pattern),
                Species.scientific_name.ilike(pattern),
            )
        )
    return db.scalars(stmt).all()


@router.get("/{species_id}", response_model=SpeciesRead)
def get_species(species_id: int, db: DbSession, user: CurrentUser):
    species = db.get(Species, species_id)
    if species is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Species not found")
    return species
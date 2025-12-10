"""Aircraft API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.models import Aircraft, AircraftCategory
from app.schemas.schemas import AircraftCreate, AircraftUpdate, AircraftResponse

router = APIRouter(prefix="/aircraft", tags=["Aircraft"])


@router.get("", response_model=List[AircraftResponse])
async def list_aircraft(
    category: Optional[AircraftCategory] = None,
    search: Optional[str] = Query(None, description="Search by tail number or owner"),
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all aircraft with optional filtering."""
    query = select(Aircraft)
    
    if category:
        query = query.where(Aircraft.category == category)
    
    if is_active is not None:
        query = query.where(Aircraft.is_active == is_active)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Aircraft.tail_number.ilike(search_term)) |
            (Aircraft.owner_name.ilike(search_term)) |
            (Aircraft.manufacturer.ilike(search_term)) |
            (Aircraft.model.ilike(search_term))
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{aircraft_id}", response_model=AircraftResponse)
async def get_aircraft(aircraft_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific aircraft by ID."""
    result = await db.execute(select(Aircraft).where(Aircraft.id == aircraft_id))
    aircraft = result.scalar_one_or_none()
    if not aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return aircraft


@router.get("/tail/{tail_number}", response_model=AircraftResponse)
async def get_aircraft_by_tail(tail_number: str, db: AsyncSession = Depends(get_db)):
    """Get aircraft by tail number."""
    result = await db.execute(
        select(Aircraft).where(Aircraft.tail_number == tail_number.upper())
    )
    aircraft = result.scalar_one_or_none()
    if not aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return aircraft


@router.post("", response_model=AircraftResponse, status_code=201)
async def create_aircraft(aircraft: AircraftCreate, db: AsyncSession = Depends(get_db)):
    """Register a new aircraft."""
    # Check for duplicate
    existing = await db.execute(
        select(Aircraft).where(Aircraft.tail_number == aircraft.tail_number.upper())
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Aircraft with this tail number already exists")
    
    db_aircraft = Aircraft(**aircraft.model_dump())
    db_aircraft.tail_number = db_aircraft.tail_number.upper()
    db.add(db_aircraft)
    await db.commit()
    await db.refresh(db_aircraft)
    return db_aircraft


@router.patch("/{aircraft_id}", response_model=AircraftResponse)
async def update_aircraft(
    aircraft_id: int,
    aircraft: AircraftUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an aircraft."""
    result = await db.execute(select(Aircraft).where(Aircraft.id == aircraft_id))
    db_aircraft = result.scalar_one_or_none()
    if not db_aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    
    update_data = aircraft.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_aircraft, field, value)
    
    await db.commit()
    await db.refresh(db_aircraft)
    return db_aircraft


@router.delete("/{aircraft_id}", status_code=204)
async def delete_aircraft(aircraft_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an aircraft."""
    result = await db.execute(select(Aircraft).where(Aircraft.id == aircraft_id))
    aircraft = result.scalar_one_or_none()
    if not aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    
    await db.delete(aircraft)
    await db.commit()

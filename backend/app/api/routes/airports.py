"""Airport API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.models import Airport
from app.schemas.schemas import AirportCreate, AirportUpdate, AirportResponse

router = APIRouter(prefix="/airports", tags=["Airports"])


@router.get("", response_model=List[AirportResponse])
async def list_airports(
    state: Optional[str] = Query(None, description="Filter by state"),
    search: Optional[str] = Query(None, description="Search by name or code"),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all airports with optional filtering."""
    query = select(Airport)
    
    if state:
        query = query.where(Airport.state == state.upper())
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Airport.name.ilike(search_term)) |
            (Airport.icao_code.ilike(search_term)) |
            (Airport.faa_code.ilike(search_term)) |
            (Airport.city.ilike(search_term))
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{airport_id}", response_model=AirportResponse)
async def get_airport(airport_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific airport by ID."""
    result = await db.execute(select(Airport).where(Airport.id == airport_id))
    airport = result.scalar_one_or_none()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    return airport


@router.get("/code/{icao_code}", response_model=AirportResponse)
async def get_airport_by_code(icao_code: str, db: AsyncSession = Depends(get_db)):
    """Get airport by ICAO code."""
    result = await db.execute(
        select(Airport).where(Airport.icao_code == icao_code.upper())
    )
    airport = result.scalar_one_or_none()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    return airport


@router.post("", response_model=AirportResponse, status_code=201)
async def create_airport(airport: AirportCreate, db: AsyncSession = Depends(get_db)):
    """Create a new airport."""
    # Check for duplicate
    existing = await db.execute(
        select(Airport).where(Airport.icao_code == airport.icao_code.upper())
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Airport with this ICAO code already exists")
    
    db_airport = Airport(**airport.model_dump())
    db_airport.icao_code = db_airport.icao_code.upper()
    db.add(db_airport)
    await db.commit()
    await db.refresh(db_airport)
    return db_airport


@router.patch("/{airport_id}", response_model=AirportResponse)
async def update_airport(
    airport_id: int,
    airport: AirportUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an airport."""
    result = await db.execute(select(Airport).where(Airport.id == airport_id))
    db_airport = result.scalar_one_or_none()
    if not db_airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    
    update_data = airport.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_airport, field, value)
    
    await db.commit()
    await db.refresh(db_airport)
    return db_airport


@router.delete("/{airport_id}", status_code=204)
async def delete_airport(airport_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an airport."""
    result = await db.execute(select(Airport).where(Airport.id == airport_id))
    airport = result.scalar_one_or_none()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    
    await db.delete(airport)
    await db.commit()

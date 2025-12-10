"""Pilot API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.models import Pilot, PilotCertificate
from app.schemas.schemas import PilotCreate, PilotUpdate, PilotResponse

router = APIRouter(prefix="/pilots", tags=["Pilots"])


@router.get("", response_model=List[PilotResponse])
async def list_pilots(
    certificate_type: Optional[PilotCertificate] = None,
    search: Optional[str] = Query(None, description="Search by name or certificate number"),
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all pilots with optional filtering."""
    query = select(Pilot)
    
    if certificate_type:
        query = query.where(Pilot.certificate_type == certificate_type)
    
    if is_active is not None:
        query = query.where(Pilot.is_active == is_active)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Pilot.first_name.ilike(search_term)) |
            (Pilot.last_name.ilike(search_term)) |
            (Pilot.certificate_number.ilike(search_term))
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{pilot_id}", response_model=PilotResponse)
async def get_pilot(pilot_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific pilot by ID."""
    result = await db.execute(select(Pilot).where(Pilot.id == pilot_id))
    pilot = result.scalar_one_or_none()
    if not pilot:
        raise HTTPException(status_code=404, detail="Pilot not found")
    return pilot


@router.get("/certificate/{certificate_number}", response_model=PilotResponse)
async def get_pilot_by_certificate(certificate_number: str, db: AsyncSession = Depends(get_db)):
    """Get pilot by certificate number."""
    result = await db.execute(
        select(Pilot).where(Pilot.certificate_number == certificate_number)
    )
    pilot = result.scalar_one_or_none()
    if not pilot:
        raise HTTPException(status_code=404, detail="Pilot not found")
    return pilot


@router.post("", response_model=PilotResponse, status_code=201)
async def create_pilot(pilot: PilotCreate, db: AsyncSession = Depends(get_db)):
    """Register a new pilot."""
    # Check for duplicate
    existing = await db.execute(
        select(Pilot).where(Pilot.certificate_number == pilot.certificate_number)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Pilot with this certificate number already exists")
    
    db_pilot = Pilot(**pilot.model_dump())
    db.add(db_pilot)
    await db.commit()
    await db.refresh(db_pilot)
    return db_pilot


@router.patch("/{pilot_id}", response_model=PilotResponse)
async def update_pilot(
    pilot_id: int,
    pilot: PilotUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a pilot."""
    result = await db.execute(select(Pilot).where(Pilot.id == pilot_id))
    db_pilot = result.scalar_one_or_none()
    if not db_pilot:
        raise HTTPException(status_code=404, detail="Pilot not found")
    
    update_data = pilot.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pilot, field, value)
    
    await db.commit()
    await db.refresh(db_pilot)
    return db_pilot


@router.delete("/{pilot_id}", status_code=204)
async def delete_pilot(pilot_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a pilot."""
    result = await db.execute(select(Pilot).where(Pilot.id == pilot_id))
    pilot = result.scalar_one_or_none()
    if not pilot:
        raise HTTPException(status_code=404, detail="Pilot not found")
    
    await db.delete(pilot)
    await db.commit()

"""Flight API routes."""
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.models import Flight, Airport, Aircraft, Pilot
from app.schemas.schemas import FlightCreate, FlightUpdate, FlightResponse

router = APIRouter(prefix="/flights", tags=["Flights"])


@router.get("/pilot-history/{pilot_id}", response_model=List[FlightResponse])
async def get_pilot_flight_history(
    pilot_id: int,
    years_back: int = Query(10, ge=1, le=50, description="Number of years to look back"),
    skip: int = 0,
    limit: int = Query(500, le=5000, description="Max results to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get complete flight history for a specific pilot.
    Defaults to last 10 years but can be extended up to 50 years.
    """
    # Verify pilot exists
    pilot_result = await db.execute(select(Pilot).where(Pilot.id == pilot_id))
    pilot = pilot_result.scalar_one_or_none()
    if not pilot:
        raise HTTPException(status_code=404, detail="Pilot not found")
    
    lookback_date = datetime.now() - timedelta(days=years_back * 365)
    
    query = select(Flight).options(
        selectinload(Flight.airport),
        selectinload(Flight.aircraft),
        selectinload(Flight.pilot_in_command)
    ).where(
        and_(
            Flight.pic_id == pilot_id,
            Flight.actual_time >= lookback_date
        )
    ).order_by(Flight.actual_time.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    flights = result.scalars().all()
    
    response = []
    for flight in flights:
        flight_dict = {
            "id": flight.id,
            "airport_id": flight.airport_id,
            "aircraft_id": flight.aircraft_id,
            "pic_id": flight.pic_id,
            "flight_type": flight.flight_type,
            "operation": flight.operation,
            "runway": flight.runway,
            "scheduled_time": flight.scheduled_time,
            "actual_time": flight.actual_time,
            "origin_airport": flight.origin_airport,
            "destination_airport": flight.destination_airport,
            "passengers": flight.passengers,
            "cargo_weight_lbs": flight.cargo_weight_lbs,
            "fuel_gallons": flight.fuel_gallons,
            "remarks": flight.remarks,
            "squawk_code": flight.squawk_code,
            "created_at": flight.created_at,
            "updated_at": flight.updated_at,
            "airport": flight.airport,
            "aircraft": flight.aircraft,
            "pilot": flight.pilot_in_command
        }
        response.append(flight_dict)
    
    return response


@router.get("", response_model=List[FlightResponse])
async def list_flights(
    airport_id: Optional[int] = None,
    aircraft_id: Optional[int] = None,
    pilot_id: Optional[int] = None,
    pilot_name: Optional[str] = Query(None, description="Search by pilot name (first or last)"),
    flight_type: Optional[str] = None,
    operation: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    years_back: Optional[int] = Query(None, description="Number of years to look back (e.g., 10 for 10 years)"),
    skip: int = 0,
    limit: int = Query(100, le=1000, description="Max results to return (up to 1000)"),
    db: AsyncSession = Depends(get_db)
):
    """List flights with optional filtering. Supports pilot name search and historical lookback."""
    query = select(Flight).options(
        selectinload(Flight.airport),
        selectinload(Flight.aircraft),
        selectinload(Flight.pilot_in_command)
    )
    
    conditions = []
    if airport_id:
        conditions.append(Flight.airport_id == airport_id)
    if aircraft_id:
        conditions.append(Flight.aircraft_id == aircraft_id)
    if pilot_id:
        conditions.append(Flight.pic_id == pilot_id)
    if flight_type:
        conditions.append(Flight.flight_type == flight_type)
    if operation:
        conditions.append(Flight.operation == operation)
    
    # Handle date range - years_back takes precedence over date_from if both provided
    if years_back:
        lookback_date = datetime.now() - timedelta(days=years_back * 365)
        conditions.append(Flight.actual_time >= lookback_date)
    elif date_from:
        conditions.append(Flight.actual_time >= date_from)
    
    if date_to:
        conditions.append(Flight.actual_time <= date_to)
    
    # Pilot name search - join with Pilot table
    if pilot_name:
        search_term = f"%{pilot_name}%"
        query = query.join(Pilot, Flight.pic_id == Pilot.id).where(
            or_(
                Pilot.first_name.ilike(search_term),
                Pilot.last_name.ilike(search_term),
                func.concat(Pilot.first_name, ' ', Pilot.last_name).ilike(search_term)
            )
        )
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.order_by(Flight.actual_time.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    flights = result.scalars().all()
    
    # Map pilot relationship
    response = []
    for flight in flights:
        flight_dict = {
            "id": flight.id,
            "airport_id": flight.airport_id,
            "aircraft_id": flight.aircraft_id,
            "pic_id": flight.pic_id,
            "flight_type": flight.flight_type,
            "operation": flight.operation,
            "runway": flight.runway,
            "scheduled_time": flight.scheduled_time,
            "actual_time": flight.actual_time,
            "origin_airport": flight.origin_airport,
            "destination_airport": flight.destination_airport,
            "passengers": flight.passengers,
            "cargo_weight_lbs": flight.cargo_weight_lbs,
            "fuel_gallons": flight.fuel_gallons,
            "remarks": flight.remarks,
            "squawk_code": flight.squawk_code,
            "created_at": flight.created_at,
            "updated_at": flight.updated_at,
            "airport": flight.airport,
            "aircraft": flight.aircraft,
            "pilot": flight.pilot_in_command
        }
        response.append(flight_dict)
    
    return response


@router.get("/{flight_id}", response_model=FlightResponse)
async def get_flight(flight_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific flight by ID."""
    query = select(Flight).where(Flight.id == flight_id).options(
        selectinload(Flight.airport),
        selectinload(Flight.aircraft),
        selectinload(Flight.pilot_in_command)
    )
    result = await db.execute(query)
    flight = result.scalar_one_or_none()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    return {
        **flight.__dict__,
        "airport": flight.airport,
        "aircraft": flight.aircraft,
        "pilot": flight.pilot_in_command
    }


@router.post("", response_model=FlightResponse, status_code=201)
async def create_flight(flight: FlightCreate, db: AsyncSession = Depends(get_db)):
    """Log a new flight (takeoff/landing)."""
    # Verify foreign keys exist
    airport = await db.execute(select(Airport).where(Airport.id == flight.airport_id))
    if not airport.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Airport not found")
    
    aircraft = await db.execute(select(Aircraft).where(Aircraft.id == flight.aircraft_id))
    if not aircraft.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Aircraft not found")
    
    pilot = await db.execute(select(Pilot).where(Pilot.id == flight.pic_id))
    if not pilot.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Pilot not found")
    
    db_flight = Flight(**flight.model_dump())
    if not db_flight.actual_time:
        db_flight.actual_time = datetime.utcnow()
    
    db.add(db_flight)
    await db.commit()
    await db.refresh(db_flight)
    
    # Load relationships
    query = select(Flight).where(Flight.id == db_flight.id).options(
        selectinload(Flight.airport),
        selectinload(Flight.aircraft),
        selectinload(Flight.pilot_in_command)
    )
    result = await db.execute(query)
    flight = result.scalar_one()
    
    return {
        **flight.__dict__,
        "airport": flight.airport,
        "aircraft": flight.aircraft,
        "pilot": flight.pilot_in_command
    }


@router.patch("/{flight_id}", response_model=FlightResponse)
async def update_flight(
    flight_id: int,
    flight: FlightUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a flight record."""
    result = await db.execute(select(Flight).where(Flight.id == flight_id))
    db_flight = result.scalar_one_or_none()
    if not db_flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    update_data = flight.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_flight, field, value)
    
    await db.commit()
    await db.refresh(db_flight)
    return db_flight


@router.delete("/{flight_id}", status_code=204)
async def delete_flight(flight_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a flight record."""
    result = await db.execute(select(Flight).where(Flight.id == flight_id))
    flight = result.scalar_one_or_none()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    await db.delete(flight)
    await db.commit()

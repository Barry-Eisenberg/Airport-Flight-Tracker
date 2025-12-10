"""Dashboard API routes."""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.models import Flight, Airport, Aircraft, Pilot
from app.schemas.schemas import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Get dashboard statistics."""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    
    # Total flights today
    flights_today = await db.execute(
        select(func.count(Flight.id)).where(Flight.actual_time >= today_start)
    )
    total_flights_today = flights_today.scalar() or 0
    
    # Total flights this week
    flights_week = await db.execute(
        select(func.count(Flight.id)).where(Flight.actual_time >= week_start)
    )
    total_flights_week = flights_week.scalar() or 0
    
    # Total aircraft
    aircraft_count = await db.execute(
        select(func.count(Aircraft.id)).where(Aircraft.is_active == True)
    )
    total_aircraft = aircraft_count.scalar() or 0
    
    # Total pilots
    pilots_count = await db.execute(
        select(func.count(Pilot.id)).where(Pilot.is_active == True)
    )
    total_pilots = pilots_count.scalar() or 0
    
    # Total airports
    airports_count = await db.execute(select(func.count(Airport.id)))
    total_airports = airports_count.scalar() or 0
    
    # Recent flights (last 10)
    recent_query = select(Flight).options(
        selectinload(Flight.airport),
        selectinload(Flight.aircraft),
        selectinload(Flight.pilot_in_command)
    ).order_by(Flight.actual_time.desc()).limit(10)
    recent_result = await db.execute(recent_query)
    recent_flights_raw = recent_result.scalars().all()
    
    recent_flights = []
    for flight in recent_flights_raw:
        recent_flights.append({
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
        })
    
    # Busiest airports (by flight count this week)
    busiest_query = select(
        Airport.id,
        Airport.icao_code,
        Airport.name,
        func.count(Flight.id).label("flight_count")
    ).join(Flight, Flight.airport_id == Airport.id).where(
        Flight.actual_time >= week_start
    ).group_by(Airport.id).order_by(func.count(Flight.id).desc()).limit(5)
    
    busiest_result = await db.execute(busiest_query)
    busiest_airports = [
        {
            "id": row.id,
            "icao_code": row.icao_code,
            "name": row.name,
            "flight_count": row.flight_count
        }
        for row in busiest_result.all()
    ]
    
    return DashboardStats(
        total_flights_today=total_flights_today,
        total_flights_week=total_flights_week,
        total_aircraft=total_aircraft,
        total_pilots=total_pilots,
        total_airports=total_airports,
        recent_flights=recent_flights,
        busiest_airports=busiest_airports
    )

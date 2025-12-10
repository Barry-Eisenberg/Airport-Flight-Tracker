"""Pydantic schemas for API validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.models import AircraftCategory, PilotCertificate, FlightType


# Airport Schemas
class AirportBase(BaseModel):
    """Base airport schema."""
    icao_code: str = Field(..., min_length=3, max_length=4)
    faa_code: Optional[str] = None
    name: str
    city: str
    state: str = Field(..., min_length=2, max_length=2)
    county: Optional[str] = None
    latitude: float
    longitude: float
    elevation_ft: Optional[int] = None
    airport_type: str = "public"
    ownership: Optional[str] = None
    runways: Optional[str] = None
    fuel_types: Optional[str] = None
    has_tower: bool = False
    ctaf_frequency: Optional[str] = None


class AirportCreate(AirportBase):
    """Schema for creating an airport."""
    pass


class AirportUpdate(BaseModel):
    """Schema for updating an airport."""
    name: Optional[str] = None
    fuel_types: Optional[str] = None
    has_tower: Optional[bool] = None
    ctaf_frequency: Optional[str] = None


class AirportResponse(AirportBase):
    """Schema for airport response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Aircraft Schemas
class AircraftBase(BaseModel):
    """Base aircraft schema."""
    tail_number: str = Field(..., min_length=1, max_length=10)
    manufacturer: str
    model: str
    year_built: Optional[int] = None
    category: AircraftCategory
    engine_type: Optional[str] = None
    num_engines: int = 1
    max_passengers: Optional[int] = None
    owner_name: str
    owner_address: Optional[str] = None
    owner_city: Optional[str] = None
    owner_state: Optional[str] = None
    is_active: bool = True


class AircraftCreate(AircraftBase):
    """Schema for creating an aircraft."""
    pass


class AircraftUpdate(BaseModel):
    """Schema for updating an aircraft."""
    owner_name: Optional[str] = None
    owner_address: Optional[str] = None
    owner_city: Optional[str] = None
    owner_state: Optional[str] = None
    is_active: Optional[bool] = None


class AircraftResponse(AircraftBase):
    """Schema for aircraft response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Pilot Schemas
class PilotBase(BaseModel):
    """Base pilot schema."""
    certificate_number: str
    first_name: str
    last_name: str
    certificate_type: PilotCertificate
    ratings: Optional[str] = None
    medical_class: Optional[str] = None
    medical_expiry: Optional[datetime] = None
    total_flight_hours: float = 0.0
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    is_active: bool = True


class PilotCreate(PilotBase):
    """Schema for creating a pilot."""
    pass


class PilotUpdate(BaseModel):
    """Schema for updating a pilot."""
    certificate_type: Optional[PilotCertificate] = None
    ratings: Optional[str] = None
    medical_class: Optional[str] = None
    medical_expiry: Optional[datetime] = None
    total_flight_hours: Optional[float] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class PilotResponse(PilotBase):
    """Schema for pilot response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Flight Schemas
class FlightBase(BaseModel):
    """Base flight schema."""
    airport_id: int
    aircraft_id: int
    pic_id: int
    flight_type: FlightType
    operation: str  # takeoff, landing, touch_and_go
    runway: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    actual_time: Optional[datetime] = None
    origin_airport: Optional[str] = None
    destination_airport: Optional[str] = None
    passengers: int = 0
    cargo_weight_lbs: Optional[float] = None
    fuel_gallons: Optional[float] = None
    remarks: Optional[str] = None
    squawk_code: Optional[str] = None


class FlightCreate(FlightBase):
    """Schema for creating a flight."""
    pass


class FlightUpdate(BaseModel):
    """Schema for updating a flight."""
    actual_time: Optional[datetime] = None
    runway: Optional[str] = None
    passengers: Optional[int] = None
    remarks: Optional[str] = None


class FlightResponse(FlightBase):
    """Schema for flight response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Nested info
    airport: Optional[AirportResponse] = None
    aircraft: Optional[AircraftResponse] = None
    pilot: Optional[PilotResponse] = None

    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardStats(BaseModel):
    """Dashboard statistics."""
    total_flights_today: int
    total_flights_week: int
    total_aircraft: int
    total_pilots: int
    total_airports: int
    recent_flights: List[FlightResponse]
    busiest_airports: List[dict]

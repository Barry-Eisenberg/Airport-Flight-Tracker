"""SQLAlchemy models for Airport Flight Tracker."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base


class AircraftCategory(str, enum.Enum):
    """Aircraft category types."""
    SINGLE_ENGINE = "single_engine"
    MULTI_ENGINE = "multi_engine"
    JET = "jet"
    HELICOPTER = "helicopter"
    GLIDER = "glider"
    BALLOON = "balloon"
    OTHER = "other"


class PilotCertificate(str, enum.Enum):
    """Pilot certificate types."""
    STUDENT = "student"
    SPORT = "sport"
    RECREATIONAL = "recreational"
    PRIVATE = "private"
    COMMERCIAL = "commercial"
    ATP = "atp"  # Airline Transport Pilot


class FlightType(str, enum.Enum):
    """Types of flight operations."""
    LOCAL = "local"
    CROSS_COUNTRY = "cross_country"
    TRAINING = "training"
    PLEASURE = "pleasure"
    BUSINESS = "business"
    CHARTER = "charter"
    CARGO = "cargo"
    MAINTENANCE = "maintenance"
    OTHER = "other"


class Airport(Base):
    """Airport model - FAA data for regional/municipal airports."""
    __tablename__ = "airports"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    icao_code: Mapped[str] = mapped_column(String(4), unique=True, index=True)
    faa_code: Mapped[Optional[str]] = mapped_column(String(4), index=True)
    name: Mapped[str] = mapped_column(String(200))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(2))
    county: Mapped[Optional[str]] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    elevation_ft: Mapped[Optional[int]] = mapped_column(Integer)
    airport_type: Mapped[str] = mapped_column(String(50))  # public, private, military
    ownership: Mapped[Optional[str]] = mapped_column(String(50))
    runways: Mapped[Optional[str]] = mapped_column(Text)  # JSON string of runway info
    fuel_types: Mapped[Optional[str]] = mapped_column(String(100))
    has_tower: Mapped[bool] = mapped_column(Boolean, default=False)
    ctaf_frequency: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Relationships
    flights: Mapped[list["Flight"]] = relationship("Flight", back_populates="airport")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Aircraft(Base):
    """Aircraft registry model."""
    __tablename__ = "aircraft"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tail_number: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    manufacturer: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))
    year_built: Mapped[Optional[int]] = mapped_column(Integer)
    category: Mapped[AircraftCategory] = mapped_column(Enum(AircraftCategory))
    engine_type: Mapped[Optional[str]] = mapped_column(String(50))
    num_engines: Mapped[int] = mapped_column(Integer, default=1)
    max_passengers: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Owner info
    owner_name: Mapped[str] = mapped_column(String(200))
    owner_address: Mapped[Optional[str]] = mapped_column(Text)
    owner_city: Mapped[Optional[str]] = mapped_column(String(100))
    owner_state: Mapped[Optional[str]] = mapped_column(String(2))
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    flights: Mapped[list["Flight"]] = relationship("Flight", back_populates="aircraft")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Pilot(Base):
    """Pilot information model."""
    __tablename__ = "pilots"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    certificate_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    certificate_type: Mapped[PilotCertificate] = mapped_column(Enum(PilotCertificate))
    ratings: Mapped[Optional[str]] = mapped_column(Text)  # JSON string of ratings
    medical_class: Mapped[Optional[str]] = mapped_column(String(20))
    medical_expiry: Mapped[Optional[datetime]] = mapped_column(DateTime)
    total_flight_hours: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Contact
    email: Mapped[Optional[str]] = mapped_column(String(200))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    state: Mapped[Optional[str]] = mapped_column(String(2))
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    flights_as_pic: Mapped[list["Flight"]] = relationship(
        "Flight", 
        back_populates="pilot_in_command",
        foreign_keys="Flight.pic_id"
    )
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Flight(Base):
    """Flight log model - tracks individual takeoffs and landings."""
    __tablename__ = "flights"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    airport_id: Mapped[int] = mapped_column(Integer, ForeignKey("airports.id"), index=True)
    aircraft_id: Mapped[int] = mapped_column(Integer, ForeignKey("aircraft.id"), index=True)
    pic_id: Mapped[int] = mapped_column(Integer, ForeignKey("pilots.id"), index=True)
    
    # Flight details
    flight_type: Mapped[FlightType] = mapped_column(Enum(FlightType))
    operation: Mapped[str] = mapped_column(String(20))  # takeoff, landing, touch_and_go
    runway: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Timestamps
    scheduled_time: Mapped[Optional[datetime]] = mapped_column(DateTime)
    actual_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Origin/Destination for tracking
    origin_airport: Mapped[Optional[str]] = mapped_column(String(4))  # ICAO code
    destination_airport: Mapped[Optional[str]] = mapped_column(String(4))
    
    # Manifest info
    passengers: Mapped[int] = mapped_column(Integer, default=0)
    cargo_weight_lbs: Mapped[Optional[float]] = mapped_column(Float)
    fuel_gallons: Mapped[Optional[float]] = mapped_column(Float)
    
    # Notes
    remarks: Mapped[Optional[str]] = mapped_column(Text)
    squawk_code: Mapped[Optional[str]] = mapped_column(String(4))
    
    # Relationships
    airport: Mapped["Airport"] = relationship("Airport", back_populates="flights")
    aircraft: Mapped["Aircraft"] = relationship("Aircraft", back_populates="flights")
    pilot_in_command: Mapped["Pilot"] = relationship(
        "Pilot", 
        back_populates="flights_as_pic",
        foreign_keys=[pic_id]
    )
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

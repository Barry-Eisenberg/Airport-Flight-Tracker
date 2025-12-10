"""Airport Flight Tracker - FastAPI Backend"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_tables
from app.core.config import get_settings
from app.api.routes import airports, flights, aircraft, pilots, dashboard

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    await create_tables()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Airport Flight Tracker",
    description="Track takeoffs, landings, and flight manifests at regional airports",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration - allow frontend URL from environment
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    settings.FRONTEND_URL,
]
# Also allow Railway's auto-generated domains
if os.environ.get("RAILWAY_PUBLIC_DOMAIN"):
    allowed_origins.append(f"https://{os.environ.get('RAILWAY_PUBLIC_DOMAIN')}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(airports.router, prefix="/api/v1")
app.include_router(flights.router, prefix="/api/v1")
app.include_router(aircraft.router, prefix="/api/v1")
app.include_router(pilots.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "airport-flight-tracker"}


@app.post("/api/v1/seed")
async def seed_database():
    """Seed the database with sample data."""
    from seed_data import seed_database as run_seed
    await run_seed()
    return {"status": "success", "message": "Database seeded with sample data"}

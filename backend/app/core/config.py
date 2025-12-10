"""Application configuration."""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Database - supports both SQLite (dev) and PostgreSQL (prod)
    # Railway provides DATABASE_URL automatically when you add PostgreSQL
    DATABASE_URL: str = "sqlite+aiosqlite:///./airport_tracker.db"
    
    # Security - MUST change in production
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    DEBUG: bool = False
    
    # CORS - Frontend URL for production
    FRONTEND_URL: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"
        extra = "ignore"
    
    @property
    def database_url(self) -> str:
        """Get the database URL, converting Railway's postgres:// to postgresql+asyncpg://"""
        url = self.DATABASE_URL
        # Railway uses postgres:// but SQLAlchemy needs postgresql+asyncpg://
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()

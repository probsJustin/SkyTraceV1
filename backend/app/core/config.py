"""
Configuration settings for the SkyTrace application
"""
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    DATABASE_URL: str = Field(
        default="postgresql://skytrace:skytrace_dev@localhost:5432/skytrace",
        description="PostgreSQL database connection string"
    )
    
    ENVIRONMENT: str = Field(default="development", description="Environment name")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # CORS settings
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    # Feature flags
    MULTI_TENANT_ENABLED: bool = Field(default=False, description="Enable multi-tenant mode")
    SSO_ENABLED: bool = Field(default=False, description="Enable SSO authentication")
    
    # Data collection settings
    DEFAULT_REFRESH_INTERVAL: int = Field(default=60, description="Default data refresh interval in seconds")
    MAX_AIRCRAFT_AGE: int = Field(default=300, description="Maximum age for aircraft data in seconds")
    
    # ADSBExchange API settings
    ADSBEXCHANGE_RAPIDAPI_KEY: str = Field(
        default="0fd6c7c2f8msh8db404e19ba5c2ap1bdc98jsn5e2e3bda3527", 
        description="RapidAPI key for ADSBExchange"
    )
    
    # Security settings
    SECRET_KEY: str = Field(default="dev-secret-key", description="Secret key for JWT tokens")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration time")
    
    # Redis settings (for future use with Celery)
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis connection string")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
"""
Simple configuration settings for testing
"""
import os
from typing import List


class Settings:
    """Simple application settings"""
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://skytrace:skytrace_dev@localhost:5432/skytrace"
    )
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000", 
        "http://localhost:8000"
    ]
    
    # Feature flags
    MULTI_TENANT_ENABLED: bool = False
    SSO_ENABLED: bool = False
    
    # Data collection settings
    DEFAULT_REFRESH_INTERVAL: int = 60
    MAX_AIRCRAFT_AGE: int = 300
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


settings = Settings()
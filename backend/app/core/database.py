"""
Database configuration and connection management
"""
from typing import AsyncGenerator

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Convert PostgreSQL URL to async format
async_database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine with error handling
try:
    async_engine = create_async_engine(
        async_database_url,
        echo=settings.ENVIRONMENT == "development",
        future=True,
        pool_pre_ping=True,
    )
except Exception as e:
    logger.warning(f"Failed to create async engine: {e}. Database features will be limited.")
    async_engine = None

# Create async session maker
if async_engine:
    AsyncSessionLocal = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
else:
    AsyncSessionLocal = None

# Create sync engine for Alembic migrations
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    future=True,
    pool_pre_ping=True,
)

# Create sync session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Base class for models
Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session"""
    if not AsyncSessionLocal:
        raise HTTPException(status_code=503, detail="Database not available")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error("Database session error", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_session():
    """Get sync database session for migrations and initial setup"""
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        logger.error("Sync database session error", error=str(e))
        session.rollback()
        raise
    finally:
        session.close()


async def init_db():
    """Initialize database"""
    if not async_engine:
        logger.warning("Database not available - skipping initialization")
        return
        
    try:
        async with async_engine.begin() as conn:
            # Import all models to ensure they are registered
            from app.models import aircraft, tenant, user, feature_flag, data_source, map_layer
            logger.info("Database connection established successfully")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise
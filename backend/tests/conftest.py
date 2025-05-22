"""
Pytest configuration and fixtures
"""
import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_async_session
from app.core.config import settings
from app.models import tenant, user, feature_flag, data_source, aircraft, map_layer


# Test database URL - use in-memory SQLite for unit tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_engine():
    """Create async test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create async test database session"""
    async_session_maker = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def test_tenant(async_session):
    """Create a test tenant"""
    from app.models.tenant import Tenant
    
    tenant_obj = Tenant(
        name="Test Tenant",
        slug="test-tenant",
        is_active=True
    )
    async_session.add(tenant_obj)
    await async_session.commit()
    await async_session.refresh(tenant_obj)
    return tenant_obj


@pytest.fixture
def override_get_async_session(async_session):
    """Override the get_async_session dependency for testing"""
    async def _override_get_async_session():
        yield async_session
    
    return _override_get_async_session


@pytest.fixture
def sample_aircraft_data():
    """Sample aircraft data for testing"""
    return {
        "hex": "ae1460",
        "type": "adsb_icao",
        "flight": "TEST123",
        "registration": "N123AB",
        "aircraft_type_code": "B738",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "altitude_baro": 10000,
        "ground_speed": 250.5,
        "track": 90.0,
        "squawk": "2000",
        "emergency": "none",
        "category": "A3"
    }


@pytest.fixture
def sample_aircraft_bulk_data():
    """Sample bulk aircraft data for testing"""
    return [
        {
            "hex": "ae1460",
            "type": "adsb_icao",
            "flight": "TEST123",
            "r": "N123AB",
            "t": "B738",
            "lat": 37.7749,
            "lon": -122.4194,
            "alt_baro": 10000,
            "gs": 250.5,
            "track": 90.0,
            "squawk": "2000",
            "emergency": "none",
            "category": "A3"
        },
        {
            "hex": "ae1461",
            "type": "adsb_icao", 
            "flight": "TEST456",
            "r": "N456CD",
            "t": "A320",
            "lat": 37.7849,
            "lon": -122.4094,
            "alt_baro": 15000,
            "gs": 300.2,
            "track": 180.0,
            "squawk": "2001",
            "emergency": "none",
            "category": "A3"
        }
    ]
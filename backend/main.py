"""
SkyTrace Backend API
Main FastAPI application entry point
"""
import logging
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api.router import api_router


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    logger.info("Starting SkyTrace API", version="1.0.0")
    await init_db()
    
    # Start the scheduler service
    from app.services.scheduler_service import scheduler
    await scheduler.start()
    logger.info("Scheduler service started")
    
    yield
    
    # Stop the scheduler service
    await scheduler.stop()
    logger.info("Scheduler service stopped")
    logger.info("Shutting down SkyTrace API")


app = FastAPI(
    title="SkyTrace API",
    description="""
    ## Multi-tenant aircraft tracking and mapping API
    
    ### Features
    - **Real-time aircraft tracking** with PostGIS spatial data
    - **Multi-tenant architecture** for organization isolation  
    - **RESTful API** with automatic OpenAPI documentation
    - **GeoJSON export** for map visualization
    - **Feature flags** for runtime configuration
    - **Modular data clients** for extensible data sources
    
    ### API Documentation
    - **Interactive docs**: [/docs](/docs) (Swagger UI)
    - **Alternative docs**: [/redoc](/redoc) (ReDoc)
    - **OpenAPI Schema**: [/openapi.json](/openapi.json)
    
    ### Quick Start
    1. Check system health: `GET /health`
    2. List aircraft: `GET /api/v1/aircraft/`
    3. Get aircraft as GeoJSON: `GET /api/v1/aircraft/geojson/all`
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",  # OpenAPI JSON schema
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "skytrace-api"}


@app.get("/")
async def root():
    """
    Root endpoint - API information and navigation
    
    Returns basic API information and links to documentation.
    """
    return {
        "message": "SkyTrace API",
        "version": "1.0.0",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc", 
            "openapi_json": "/openapi.json"
        },
        "api_endpoints": {
            "health": "/health",
            "aircraft": "/api/v1/aircraft/",
            "aircraft_geojson": "/api/v1/aircraft/geojson/all",
            "map_layers": "/api/v1/map-layers/",
            "feature_flags": "/api/v1/feature-flags/",
            "scheduler_jobs": "/api/v1/scheduler/jobs/",
            "run_job": "/api/v1/scheduler/jobs/{job_id}/run"
        }
    }


@app.get("/api")
async def api_info():
    """
    API information endpoint
    
    Provides detailed information about the API and available endpoints.
    """
    return {
        "name": "SkyTrace API",
        "version": "1.0.0",
        "description": "Multi-tenant aircraft tracking and mapping API",
        "openapi_version": "3.0.0",
        "contact": {
            "name": "SkyTrace Support",
            "url": "https://github.com/your-org/skytrace"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
Main API router configuration
"""
from fastapi import APIRouter

from app.api.endpoints import aircraft, tenants, feature_flags, data_sources, map_layers, scheduler

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(aircraft.router, prefix="/aircraft", tags=["Aircraft"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(feature_flags.router, prefix="/feature-flags", tags=["Feature Flags"])
api_router.include_router(data_sources.router, prefix="/data-sources", tags=["Data Sources"])
api_router.include_router(map_layers.router, prefix="/map-layers", tags=["Map Layers"])
api_router.include_router(scheduler.router, prefix="/scheduler", tags=["Scheduler"])
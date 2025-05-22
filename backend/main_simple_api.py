"""
SkyTrace Backend API - Simple Standalone Version
FastAPI application with no database or complex dependencies
"""
import asyncio
import random
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# Simple Pydantic models for requests
class MapLayerCreate(BaseModel):
    name: str
    description: Optional[str] = None
    layer_type: str
    data_source_id: Optional[str] = None
    style_config: Optional[Dict[str, Any]] = None
    is_visible: bool = True
    is_active: bool = True
    z_index: int = 0


class MapLayerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    layer_type: Optional[str] = None
    data_source_id: Optional[str] = None
    style_config: Optional[Dict[str, Any]] = None
    is_visible: Optional[bool] = None
    is_active: Optional[bool] = None
    z_index: Optional[int] = None


class FeatureFlagUpdate(BaseModel):
    enabled: Optional[bool] = None
    description: Optional[str] = None


class AircraftCreate(BaseModel):
    hex: str = Field(..., min_length=6, max_length=6)
    type: str
    flight: Optional[str] = None
    registration: Optional[str] = None
    aircraft_type_code: Optional[str] = None
    db_flags: Optional[int] = None
    squawk: Optional[str] = None
    emergency: Optional[str] = "none"
    category: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    altitude_baro: Optional[int] = None
    altitude_geom: Optional[int] = None
    ground_speed: Optional[float] = Field(None, ge=0)
    track: Optional[float] = Field(None, ge=0, lt=360)
    true_heading: Optional[float] = Field(None, ge=0, lt=360)
    vertical_rate: Optional[int] = None
    nic: Optional[int] = None
    nac_p: Optional[int] = None
    nac_v: Optional[int] = None
    sil: Optional[int] = None
    sil_type: Optional[str] = None
    sda: Optional[int] = None
    messages: Optional[int] = None
    seen: Optional[float] = None
    seen_pos: Optional[float] = None
    rssi: Optional[float] = None
    raw_data: Optional[Dict[str, Any]] = None


class TenantCreate(BaseModel):
    name: str
    slug: str
    is_active: bool = True


class DataSourceCreate(BaseModel):
    name: str
    type: str
    client_class: str
    config: Optional[Dict[str, Any]] = None
    is_active: bool = True
    refresh_interval: int = 60


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    print("🚀 Starting SkyTrace API (Simple Demo Mode)")
    yield
    print("👋 Shutting down SkyTrace API")


app = FastAPI(
    title="SkyTrace API",
    description="""
    ## Multi-tenant Aircraft Tracking and Mapping API (Demo Mode)
    
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
    4. Manage map layers: `GET /api/v1/map-layers/`
    
    **Note**: This is running in demo mode with sample data.
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "skytrace-api", "mode": "demo"}


@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API navigation"""
    return {
        "message": "SkyTrace API",
        "version": "1.0.0",
        "mode": "demo",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc", 
            "openapi_json": "/openapi.json"
        },
        "api_endpoints": {
            "health": "/health",
            "aircraft": "/api/v1/aircraft/",
            "aircraft_geojson": "/api/v1/aircraft/geojson/all",
            "aircraft_bulk": "/api/v1/aircraft/bulk",
            "tenants": "/api/v1/tenants/",
            "map_layers": "/api/v1/map-layers/",
            "data_sources": "/api/v1/data-sources/",
            "feature_flags": "/api/v1/feature-flags/",
            "scheduler_jobs": "/api/v1/scheduler/jobs/",
            "run_job": "/api/v1/scheduler/jobs/{job_id}/run"
        }
    }


@app.get("/api", tags=["System"])
async def api_info():
    """API information endpoint"""
    return {
        "name": "SkyTrace API",
        "version": "1.0.0",
        "description": "Multi-tenant aircraft tracking and mapping API",
        "openapi_version": "3.0.0",
        "mode": "demo",
        "contact": {
            "name": "SkyTrace Support",
            "url": "https://github.com/your-org/skytrace"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    }


@app.get("/api/v1/aircraft/", tags=["Aircraft"])
async def get_aircraft(skip: int = 0, limit: int = 100):
    """Get aircraft data (demo version)"""
    return {
        "aircraft": [
            {
                "id": "demo-aircraft-1",
                "hex": "ae1460",
                "type": "adsb_icao",
                "flight": "DEMO123",
                "registration": "N123AB",
                "aircraft_type_code": "B738",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "altitude_baro": 10000,
                "ground_speed": "250.5",
                "track": "90.0",
                "squawk": "2000",
                "emergency": "none",
                "category": "A3",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
                "tenant_id": "demo"
            },
            {
                "id": "demo-aircraft-2", 
                "hex": "ae1461",
                "type": "adsb_icao",
                "flight": "DEMO456",
                "registration": "N456CD",
                "aircraft_type_code": "A320",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "altitude_baro": 15000,
                "ground_speed": "300.2",
                "track": "180.0",
                "squawk": "2001",
                "emergency": "none",
                "category": "A3",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
                "tenant_id": "demo"
            },
            {
                "id": "demo-aircraft-3",
                "hex": "ae1462",
                "type": "adsb_icao",
                "flight": "DEMO789",
                "registration": "N789EF",
                "aircraft_type_code": "B777",
                "latitude": 34.0522,
                "longitude": -118.2437,
                "altitude_baro": 35000,
                "ground_speed": "450.0",
                "track": "270.0",
                "squawk": "2002",
                "emergency": "none",
                "category": "A4",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
                "tenant_id": "demo"
            }
        ],
        "total": 3,
        "page": skip // limit + 1,
        "size": 3
    }


@app.get("/api/v1/aircraft/geojson/all", tags=["Aircraft"])
async def get_aircraft_geojson():
    """Get aircraft data as GeoJSON FeatureCollection"""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [-122.4194, 37.7749]
                },
                "properties": {
                    "id": "demo-aircraft-1",
                    "hex": "ae1460",
                    "flight": "DEMO123",
                    "registration": "N123AB",
                    "aircraft_type": "B738",
                    "altitude": 10000,
                    "speed": "250.5",
                    "track": "90.0",
                    "squawk": "2000",
                    "emergency": "none",
                    "category": "A3"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [-74.0060, 40.7128]
                },
                "properties": {
                    "id": "demo-aircraft-2",
                    "hex": "ae1461", 
                    "flight": "DEMO456",
                    "registration": "N456CD",
                    "aircraft_type": "A320",
                    "altitude": 15000,
                    "speed": "300.2",
                    "track": "180.0",
                    "squawk": "2001",
                    "emergency": "none",
                    "category": "A3"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [-118.2437, 34.0522]
                },
                "properties": {
                    "id": "demo-aircraft-3",
                    "hex": "ae1462",
                    "flight": "DEMO789",
                    "registration": "N789EF",
                    "aircraft_type": "B777",
                    "altitude": 35000,
                    "speed": "450.0",
                    "track": "270.0",
                    "squawk": "2002",
                    "emergency": "none",
                    "category": "A4"
                }
            }
        ]
    }


@app.get("/api/v1/map-layers/", tags=["Map Layers"])
async def get_map_layers():
    """Get map layers (demo version)"""
    return [
        {
            "id": "demo-layer-aircraft",
            "tenant_id": "demo",
            "name": "Aircraft",
            "description": "Live aircraft tracking data with real-time positions",
            "layer_type": "aircraft",
            "data_source_id": "demo-aircraft-source",
            "style_config": {
                "circle-radius": 6,
                "circle-color": "#4CAF50",
                "circle-stroke-width": 2,
                "circle-stroke-color": "#ffffff"
            },
            "is_visible": True,
            "is_active": True,
            "z_index": 10,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": "demo-layer-airports",
            "tenant_id": "demo", 
            "name": "Major Airports",
            "description": "Major commercial airports and airfields",
            "layer_type": "geojson",
            "data_source_id": "demo-airports-source",
            "style_config": {
                "circle-radius": 8,
                "circle-color": "#2196F3",
                "circle-stroke-width": 2,
                "circle-stroke-color": "#ffffff"
            },
            "is_visible": False,
            "is_active": True,
            "z_index": 5,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": "demo-layer-weather",
            "tenant_id": "demo",
            "name": "Weather Radar",
            "description": "Real-time weather radar overlay",
            "layer_type": "pmtiles",
            "data_source_id": "demo-weather-source",
            "style_config": {
                "raster-opacity": 0.7,
                "raster-fade-duration": 0
            },
            "is_visible": False,
            "is_active": True,
            "z_index": 1,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": "demo-layer-restricted",
            "tenant_id": "demo",
            "name": "Restricted Airspace",
            "description": "No-fly zones and restricted airspace boundaries",
            "layer_type": "geojson",
            "data_source_id": "demo-airspace-source",
            "style_config": {
                "fill-color": "#FF5722",
                "fill-opacity": 0.3,
                "line-color": "#FF5722",
                "line-width": 2
            },
            "is_visible": False,
            "is_active": True,
            "z_index": 3,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    ]


@app.post("/api/v1/map-layers/", tags=["Map Layers"])
async def create_map_layer(layer_data: MapLayerCreate):
    """Create new map layer (demo version)"""
    return {
        "id": "demo-new-layer",
        "tenant_id": "demo",
        "name": layer_data.name,
        "description": layer_data.description or "",
        "layer_type": layer_data.layer_type,
        "data_source_id": layer_data.data_source_id,
        "style_config": layer_data.style_config or {},
        "is_visible": layer_data.is_visible,
        "is_active": layer_data.is_active,
        "z_index": layer_data.z_index,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }


@app.patch("/api/v1/map-layers/{layer_id}", tags=["Map Layers"])
async def update_map_layer(layer_id: str, layer_data: MapLayerUpdate):
    """Update map layer (demo version)"""
    return {
        "id": layer_id,
        "tenant_id": "demo",
        "name": layer_data.name or "Updated Layer",
        "description": layer_data.description or "",
        "layer_type": layer_data.layer_type or "geojson",
        "data_source_id": layer_data.data_source_id,
        "style_config": layer_data.style_config or {},
        "is_visible": layer_data.is_visible if layer_data.is_visible is not None else True,
        "is_active": layer_data.is_active if layer_data.is_active is not None else True,
        "z_index": layer_data.z_index or 0,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }


@app.get("/api/v1/feature-flags/", tags=["Feature Flags"])
async def get_feature_flags():
    """Get feature flags (demo version)"""
    return [
        {
            "id": "demo-flag-sso",
            "tenant_id": "demo",
            "name": "sso_enabled",
            "enabled": False,
            "description": "Enable Single Sign-On authentication",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": "demo-flag-multi-tenant",
            "tenant_id": "demo",
            "name": "multi_tenant",
            "enabled": False,
            "description": "Enable multi-tenant functionality",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": "demo-flag-realtime",
            "tenant_id": "demo",
            "name": "realtime_updates",
            "enabled": True,
            "description": "Enable real-time data updates",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": "demo-flag-filtering",
            "tenant_id": "demo",
            "name": "advanced_filtering",
            "enabled": True,
            "description": "Enable advanced filtering options",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    ]


@app.patch("/api/v1/feature-flags/{flag_name}", tags=["Feature Flags"])
async def update_feature_flag(flag_name: str, flag_data: FeatureFlagUpdate):
    """Update feature flag (demo version)"""
    return {
        "id": f"demo-flag-{flag_name}",
        "tenant_id": "demo",
        "name": flag_name,
        "enabled": flag_data.enabled if flag_data.enabled is not None else False,
        "description": flag_data.description or f"Feature flag: {flag_name}",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }


# Additional Aircraft Endpoints
@app.get("/api/v1/aircraft/{aircraft_id}", tags=["Aircraft"])
async def get_aircraft_by_id(aircraft_id: str):
    """Get specific aircraft by ID (demo version)"""
    # Find aircraft in our demo data
    demo_aircraft = {
        "demo-aircraft-1": {
            "id": "demo-aircraft-1",
            "hex": "ae1460",
            "type": "adsb_icao",
            "flight": "DEMO123",
            "registration": "N123AB",
            "aircraft_type_code": "B738",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "altitude_baro": 10000,
            "ground_speed": "250.5",
            "track": "90.0",
            "squawk": "2000",
            "emergency": "none",
            "category": "A3",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "tenant_id": "demo"
        }
    }
    
    if aircraft_id not in demo_aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    
    return demo_aircraft[aircraft_id]


@app.post("/api/v1/aircraft/", tags=["Aircraft"])
async def create_aircraft(aircraft: AircraftCreate):
    """Create new aircraft (demo version)"""
    return {
        "id": f"demo-aircraft-{aircraft.hex}",
        "hex": aircraft.hex,
        "type": aircraft.type,
        "flight": aircraft.flight,
        "registration": aircraft.registration,
        "aircraft_type_code": aircraft.aircraft_type_code,
        "latitude": aircraft.latitude,
        "longitude": aircraft.longitude,
        "altitude_baro": aircraft.altitude_baro,
        "ground_speed": str(aircraft.ground_speed) if aircraft.ground_speed else None,
        "track": str(aircraft.track) if aircraft.track else None,
        "squawk": aircraft.squawk,
        "emergency": aircraft.emergency,
        "category": aircraft.category,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "tenant_id": "demo"
    }


@app.post("/api/v1/aircraft/bulk", tags=["Aircraft"])
async def create_bulk_aircraft(aircraft_list: List[Dict[str, Any]]):
    """Bulk create/update aircraft from raw data (demo version)"""
    processed = len(aircraft_list)
    created = len([a for a in aircraft_list if a.get("hex")])
    updated = 0
    errors = len([a for a in aircraft_list if not a.get("hex")])
    
    return {
        "processed": processed,
        "created": created, 
        "updated": updated,
        "errors": errors
    }


# Tenant Endpoints
@app.get("/api/v1/tenants/", tags=["Tenants"])
async def get_tenants():
    """Get all tenants (demo version)"""
    return [
        {
            "id": "demo-tenant-1",
            "name": "Demo Organization",
            "slug": "demo",
            "is_active": True,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": "demo-tenant-2",
            "name": "Test Aviation Corp",
            "slug": "test-aviation",
            "is_active": True,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    ]


@app.get("/api/v1/tenants/{tenant_id}", tags=["Tenants"])
async def get_tenant(tenant_id: str):
    """Get tenant by ID (demo version)"""
    if tenant_id == "demo-tenant-1":
        return {
            "id": "demo-tenant-1",
            "name": "Demo Organization",
            "slug": "demo",
            "is_active": True,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    else:
        raise HTTPException(status_code=404, detail="Tenant not found")


@app.post("/api/v1/tenants/", tags=["Tenants"])
async def create_tenant(tenant: TenantCreate):
    """Create new tenant (demo version)"""
    return {
        "id": f"demo-tenant-{tenant.slug}",
        "name": tenant.name,
        "slug": tenant.slug,
        "is_active": tenant.is_active,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }


# Data Source Endpoints
@app.get("/api/v1/data-sources/", tags=["Data Sources"])
async def get_data_sources():
    """Get all data sources (demo version)"""
    return [
        {
            "id": "demo-aircraft-source",
            "tenant_id": "demo",
            "name": "Mock Aircraft Client",
            "type": "aircraft",
            "client_class": "MockAircraftClient",
            "config": {
                "refresh_rate": 30,
                "max_aircraft": 100
            },
            "is_active": True,
            "refresh_interval": 60,
            "last_updated": "2023-01-01T00:00:00Z",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": "demo-weather-source",
            "tenant_id": "demo",
            "name": "Weather Radar Client",
            "type": "weather",
            "client_class": "WeatherRadarClient",
            "config": {
                "api_key": "demo-key",
                "layers": ["precipitation", "temperature"]
            },
            "is_active": True,
            "refresh_interval": 300,
            "last_updated": "2023-01-01T00:00:00Z",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    ]


@app.post("/api/v1/data-sources/", tags=["Data Sources"])
async def create_data_source(data_source: DataSourceCreate):
    """Create new data source (demo version)"""
    return {
        "id": f"demo-source-{data_source.name.lower().replace(' ', '-')}",
        "tenant_id": "demo",
        "name": data_source.name,
        "type": data_source.type,
        "client_class": data_source.client_class,
        "config": data_source.config or {},
        "is_active": data_source.is_active,
        "refresh_interval": data_source.refresh_interval,
        "last_updated": None,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }


@app.get("/api/v1/data-sources/{source_id}", tags=["Data Sources"])
async def get_data_source(source_id: str):
    """Get data source by ID (demo version)"""
    if source_id == "demo-aircraft-source":
        return {
            "id": "demo-aircraft-source",
            "tenant_id": "demo",
            "name": "Mock Aircraft Client",
            "type": "aircraft",
            "client_class": "MockAircraftClient",
            "config": {
                "refresh_rate": 30,
                "max_aircraft": 100
            },
            "is_active": True,
            "refresh_interval": 60,
            "last_updated": "2023-01-01T00:00:00Z",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    else:
        raise HTTPException(status_code=404, detail="Data source not found")


# Additional Map Layer Endpoints
@app.get("/api/v1/map-layers/{layer_id}", tags=["Map Layers"])
async def get_map_layer(layer_id: str):
    """Get specific map layer by ID (demo version)"""
    demo_layers = {
        "demo-layer-aircraft": {
            "id": "demo-layer-aircraft",
            "tenant_id": "demo",
            "name": "Aircraft",
            "description": "Live aircraft tracking data with real-time positions",
            "layer_type": "aircraft",
            "data_source_id": "demo-aircraft-source",
            "style_config": {
                "circle-radius": 6,
                "circle-color": "#4CAF50",
                "circle-stroke-width": 2,
                "circle-stroke-color": "#ffffff"
            },
            "is_visible": True,
            "is_active": True,
            "z_index": 10,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    }
    
    if layer_id not in demo_layers:
        raise HTTPException(status_code=404, detail="Map layer not found")
    
    return demo_layers[layer_id]


@app.delete("/api/v1/map-layers/{layer_id}", tags=["Map Layers"])
async def delete_map_layer(layer_id: str):
    """Delete map layer (demo version)"""
    return {"message": f"Map layer {layer_id} deleted successfully"}


# Test Endpoints
@app.get("/api/v1/test/mock-data")
async def generate_mock_data():
    """Generate mock test data for development"""
    import random
    
    mock_aircraft = []
    for i in range(10):
        hex_code = f"{random.randint(0, 0xFFFFFF):06x}"
        lat = 39.8283 + random.uniform(-10, 10)  # Around US center
        lon = -98.5795 + random.uniform(-20, 20)
        
        mock_aircraft.append({
            "hex": hex_code,
            "type": "adsb_icao",
            "flight": f"TEST{random.randint(100, 999)}",
            "registration": f"N{random.randint(100, 999)}AB",
            "aircraft_type_code": random.choice(["B738", "A320", "B777", "A350"]),
            "latitude": lat,
            "longitude": lon,
            "altitude_baro": random.randint(1000, 40000),
            "ground_speed": random.randint(150, 500),
            "track": random.randint(0, 359),
            "squawk": f"{random.randint(1000, 7777):04d}",
            "emergency": "none",
            "category": random.choice(["A1", "A2", "A3", "A4"])
        })
    
    return {
        "aircraft": mock_aircraft,
        "count": len(mock_aircraft),
        "generated_at": "2023-01-01T00:00:00Z"
    }


@app.get("/api/v1/test/system-info")
async def get_system_info():
    """Get system information for debugging"""
    return {
        "mode": "demo",
        "version": "1.0.0",
        "database": "disabled",
        "endpoints_available": [
            "GET /api/v1/aircraft/",
            "GET /api/v1/aircraft/{id}",
            "POST /api/v1/aircraft/",
            "POST /api/v1/aircraft/bulk",
            "GET /api/v1/aircraft/geojson/all",
            "GET /api/v1/tenants/",
            "GET /api/v1/tenants/{id}",
            "POST /api/v1/tenants/",
            "GET /api/v1/map-layers/",
            "GET /api/v1/map-layers/{id}",
            "POST /api/v1/map-layers/",
            "PATCH /api/v1/map-layers/{id}",
            "DELETE /api/v1/map-layers/{id}",
            "GET /api/v1/data-sources/",
            "GET /api/v1/data-sources/{id}",
            "POST /api/v1/data-sources/",
            "GET /api/v1/feature-flags/",
            "PATCH /api/v1/feature-flags/{name}",
            "GET /api/v1/test/mock-data",
            "GET /api/v1/test/system-info"
        ],
        "features": {
            "aircraft_tracking": True,
            "map_layers": True,
            "feature_flags": True,
            "multi_tenant": True,
            "geojson_export": True,
            "bulk_operations": True
        }
    }


# Scheduler Endpoints
@app.get("/api/v1/scheduler/jobs/", tags=["Scheduler"])
async def get_scheduled_jobs():
    """Get all scheduled data collection jobs (demo version)"""
    return [
        {
            "job_id": "adsbexchange-military",
            "name": "ADSBExchange Military Aircraft",
            "client_class": "ADSBExchangeClient",
            "config": {
                "endpoint": "/v2/mil/",
                "timeout": 30
            },
            "interval_minutes": 30,
            "tenant_id": "demo",
            "enabled": True,
            "last_run": "2023-01-01T00:00:00Z",
            "next_run": "2023-01-01T00:30:00Z",
            "run_count": 48,
            "error_count": 0,
            "last_error": None
        },
        {
            "job_id": "mock-aircraft-generator",
            "name": "Mock Aircraft Data Generator",
            "client_class": "MockAircraftClient",
            "config": {
                "count": 50,
                "area": "us"
            },
            "interval_minutes": 15,
            "tenant_id": "demo",
            "enabled": True,
            "last_run": "2023-01-01T00:15:00Z",
            "next_run": "2023-01-01T00:30:00Z",
            "run_count": 96,
            "error_count": 2,
            "last_error": None
        },
        {
            "job_id": "weather-data-collector",
            "name": "Weather Data Collection",
            "client_class": "WeatherDataClient",
            "config": {
                "regions": ["us-west", "us-east"],
                "layers": ["precipitation", "wind"]
            },
            "interval_minutes": 60,
            "tenant_id": "demo",
            "enabled": False,
            "last_run": "2023-01-01T00:00:00Z",
            "next_run": "2023-01-01T01:00:00Z",
            "run_count": 24,
            "error_count": 1,
            "last_error": "API rate limit exceeded"
        }
    ]


@app.get("/api/v1/scheduler/jobs/{job_id}", tags=["Scheduler"])
async def get_scheduled_job(job_id: str):
    """Get specific scheduled job details (demo version)"""
    demo_jobs = {
        "adsbexchange-military": {
            "job_id": "adsbexchange-military",
            "name": "ADSBExchange Military Aircraft",
            "client_class": "ADSBExchangeClient",
            "config": {
                "rapidapi_key": "***hidden***",
                "endpoint": "/v2/mil/",
                "timeout": 30
            },
            "interval_minutes": 30,
            "tenant_id": "demo",
            "enabled": True,
            "last_run": "2023-01-01T00:00:00Z",
            "next_run": "2023-01-01T00:30:00Z",
            "run_count": 48,
            "error_count": 0,
            "last_error": None,
            "description": "Collects military aircraft data from ADSBExchange RapidAPI every 30 minutes",
            "data_type": "aircraft",
            "coverage": "Global military aircraft",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    }
    
    if job_id not in demo_jobs:
        raise HTTPException(status_code=404, detail="Scheduled job not found")
    
    return demo_jobs[job_id]


@app.post("/api/v1/scheduler/jobs/{job_id}/run", tags=["Scheduler"])
async def run_job_now(job_id: str):
    """Run a scheduled job immediately (demo version)"""
    demo_jobs = ["adsbexchange-military", "mock-aircraft-generator", "weather-data-collector"]
    
    if job_id not in demo_jobs:
        raise HTTPException(status_code=404, detail="Scheduled job not found")
    
    # Simulate running the job
    import random
    import time
    
    # Simulate processing time
    await asyncio.sleep(0.5)
    
    # Simulate success/failure
    success = random.random() > 0.1  # 90% success rate
    
    result = {
        "job_id": job_id,
        "status": "completed" if success else "failed",
        "started_at": "2023-01-01T00:00:00Z",
        "completed_at": "2023-01-01T00:00:05Z",
        "duration_seconds": 5,
        "success": success
    }
    
    if success:
        result.update({
            "records_processed": random.randint(10, 100),
            "records_created": random.randint(5, 50),
            "records_updated": random.randint(0, 30),
            "records_errors": random.randint(0, 5)
        })
    else:
        result["error"] = "Connection timeout to data source"
    
    return result


@app.post("/api/v1/scheduler/jobs/", tags=["Scheduler"])
async def create_scheduled_job(job_data: Dict[str, Any]):
    """Create new scheduled job (demo version)"""
    return {
        "job_id": f"demo-job-{random.randint(1000, 9999)}",
        "name": job_data.get("name", "New Data Collection Job"),
        "client_class": job_data.get("client_class", "GenericDataClient"),
        "config": job_data.get("config", {}),
        "interval_minutes": job_data.get("interval_minutes", 60),
        "tenant_id": "demo",
        "enabled": job_data.get("enabled", True),
        "last_run": None,
        "next_run": "2023-01-01T01:00:00Z",
        "run_count": 0,
        "error_count": 0,
        "last_error": None,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }


@app.patch("/api/v1/scheduler/jobs/{job_id}", tags=["Scheduler"])
async def update_scheduled_job(job_id: str, job_data: Dict[str, Any]):
    """Update scheduled job (demo version)"""
    return {
        "job_id": job_id,
        "name": job_data.get("name", "Updated Job"),
        "enabled": job_data.get("enabled", True),
        "interval_minutes": job_data.get("interval_minutes", 60),
        "config": job_data.get("config", {}),
        "updated_at": "2023-01-01T00:00:00Z"
    }


@app.delete("/api/v1/scheduler/jobs/{job_id}", tags=["Scheduler"])
async def delete_scheduled_job(job_id: str):
    """Delete scheduled job (demo version)"""
    return {"message": f"Scheduled job {job_id} deleted successfully"}


# Test the ADSBExchange client
@app.get("/api/v1/test/adsbexchange")
async def test_adsbexchange_client():
    """Test the ADSBExchange client directly"""
    try:
        # This would normally import and run the real client
        # For demo purposes, return mock data
        return {
            "status": "success",
            "client": "ADSBExchangeClient",
            "data_source": "adsbexchange_rapidapi",
            "test_result": {
                "aircraft_count": 25,
                "sample_aircraft": [
                    {
                        "hex": "ae1460",
                        "type": "adsb_icao",
                        "flight": "MIL001",
                        "registration": "06-6162",
                        "aircraft_type_code": "C17",
                        "latitude": 38.26078,
                        "longitude": -121.944717,
                        "altitude_baro": 10000,
                        "category": "A5"
                    }
                ],
                "collection_time": "2023-01-01T00:00:00Z",
                "api_response_time": 1.2
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "client": "ADSBExchangeClient"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
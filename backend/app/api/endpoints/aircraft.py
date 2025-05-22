"""
Aircraft API endpoints
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from geoalchemy2.functions import ST_X, ST_Y
import structlog

from app.core.database import get_async_session
from app.models.aircraft import Aircraft as AircraftModel
from app.models.tenant import Tenant as TenantModel
from app.schemas.aircraft import Aircraft, AircraftCreate, AircraftUpdate, AircraftResponse
from app.services.aircraft_service import AircraftService

logger = structlog.get_logger()
router = APIRouter()


async def get_default_tenant(session: AsyncSession) -> TenantModel:
    """Get default tenant for demo purposes"""
    result = await session.execute(
        select(TenantModel).where(TenantModel.slug == "default")
    )
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Default tenant not found")
    return tenant


@router.get("/", response_model=AircraftResponse)
async def get_aircraft(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    hex_filter: Optional[str] = Query(None, alias="hex", description="Filter by aircraft hex code"),
    flight_filter: Optional[str] = Query(None, alias="flight", description="Filter by flight number"),
    session: AsyncSession = Depends(get_async_session),
):
    """Get aircraft data with pagination and filtering"""
    tenant = await get_default_tenant(session)
    
    query = select(AircraftModel).where(AircraftModel.tenant_id == tenant.id)
    
    # Apply filters
    if hex_filter:
        query = query.where(AircraftModel.hex.ilike(f"%{hex_filter}%"))
    if flight_filter:
        query = query.where(AircraftModel.flight.ilike(f"%{flight_filter}%"))
    
    # Get total count
    count_query = select(func.count(AircraftModel.id)).where(AircraftModel.tenant_id == tenant.id)
    if hex_filter:
        count_query = count_query.where(AircraftModel.hex.ilike(f"%{hex_filter}%"))
    if flight_filter:
        count_query = count_query.where(AircraftModel.flight.ilike(f"%{flight_filter}%"))
    
    total_result = await session.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination and execute with coordinate extraction
    query = query.add_columns(
        ST_X(AircraftModel.position).label('longitude'),
        ST_Y(AircraftModel.position).label('latitude')
    ).offset(skip).limit(limit).order_by(AircraftModel.last_updated.desc())
    result = await session.execute(query)
    aircraft_rows = result.fetchall()
    
    # Convert to response format
    aircraft_list = []
    for row in aircraft_rows:
        aircraft_model = row[0]  # First item is the aircraft model
        longitude = row[1] if len(row) > 1 else None  # Second item is longitude
        latitude = row[2] if len(row) > 2 else None   # Third item is latitude
        
        # If PostGIS extraction failed, try to get coordinates from raw_data
        if latitude is None and longitude is None and aircraft_model.raw_data:
            raw_data = aircraft_model.raw_data
            if isinstance(raw_data, dict):
                # Try direct latitude/longitude in raw_data
                if raw_data.get('latitude') and raw_data.get('longitude'):
                    latitude = raw_data['latitude']
                    longitude = raw_data['longitude']
                # Try lastPosition in raw_data
                elif raw_data.get('lastPosition'):
                    last_pos = raw_data['lastPosition']
                    if last_pos.get('lat') and last_pos.get('lon'):
                        latitude = last_pos['lat']
                        longitude = last_pos['lon']
                # Try nested raw_data.lastPosition
                elif raw_data.get('raw_data', {}).get('lastPosition'):
                    last_pos = raw_data['raw_data']['lastPosition']
                    if last_pos.get('lat') and last_pos.get('lon'):
                        latitude = last_pos['lat']
                        longitude = last_pos['lon']
        
        aircraft_dict = {
            "id": aircraft_model.id,
            "created_at": aircraft_model.created_at,
            "updated_at": aircraft_model.last_updated,
            "tenant_id": aircraft_model.tenant_id,
            "hex": aircraft_model.hex,
            "type": aircraft_model.type,
            "flight": aircraft_model.flight,
            "registration": aircraft_model.registration,
            "aircraft_type_code": aircraft_model.aircraft_type_code,
            "db_flags": aircraft_model.db_flags,
            "squawk": aircraft_model.squawk,
            "emergency": aircraft_model.emergency,
            "category": aircraft_model.category,
            "altitude_baro": aircraft_model.altitude_baro,
            "altitude_geom": aircraft_model.altitude_geom,
            "ground_speed": aircraft_model.ground_speed,
            "track": aircraft_model.track,
            "true_heading": aircraft_model.true_heading,
            "vertical_rate": aircraft_model.vertical_rate,
            "nic": aircraft_model.nic,
            "nac_p": aircraft_model.nac_p,
            "nac_v": aircraft_model.nac_v,
            "sil": aircraft_model.sil,
            "sil_type": aircraft_model.sil_type,
            "sda": aircraft_model.sda,
            "messages": aircraft_model.messages,
            "seen": aircraft_model.seen,
            "seen_pos": aircraft_model.seen_pos,
            "rssi": aircraft_model.rssi,
            "gps_ok_before": aircraft_model.gps_ok_before,
            "gps_ok_lat": aircraft_model.gps_ok_lat,
            "gps_ok_lon": aircraft_model.gps_ok_lon,
            "raw_data": aircraft_model.raw_data,
            "latitude": float(latitude) if latitude is not None else None,
            "longitude": float(longitude) if longitude is not None else None,
        }
        
        aircraft_list.append(Aircraft(**aircraft_dict))
    
    return AircraftResponse(
        aircraft=aircraft_list,
        total=total,
        page=skip // limit + 1,
        size=len(aircraft_list)
    )


@router.get("/{aircraft_id}", response_model=Aircraft)
async def get_aircraft_by_id(
    aircraft_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Get specific aircraft by ID"""
    tenant = await get_default_tenant(session)
    
    result = await session.execute(
        select(AircraftModel, 
               ST_X(AircraftModel.position).label('longitude'),
               ST_Y(AircraftModel.position).label('latitude')).where(
            AircraftModel.id == aircraft_id,
            AircraftModel.tenant_id == tenant.id
        )
    )
    row = result.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    
    aircraft_model = row[0]
    longitude = row[1] if len(row) > 1 else None
    latitude = row[2] if len(row) > 2 else None
    
    # If PostGIS extraction failed, try to get coordinates from raw_data
    if latitude is None and longitude is None and aircraft_model.raw_data:
        raw_data = aircraft_model.raw_data
        if isinstance(raw_data, dict):
            # Try direct latitude/longitude in raw_data
            if raw_data.get('latitude') and raw_data.get('longitude'):
                latitude = raw_data['latitude']
                longitude = raw_data['longitude']
            # Try lastPosition in raw_data
            elif raw_data.get('lastPosition'):
                last_pos = raw_data['lastPosition']
                if last_pos.get('lat') and last_pos.get('lon'):
                    latitude = last_pos['lat']
                    longitude = last_pos['lon']
            # Try nested raw_data.lastPosition
            elif raw_data.get('raw_data', {}).get('lastPosition'):
                last_pos = raw_data['raw_data']['lastPosition']
                if last_pos.get('lat') and last_pos.get('lon'):
                    latitude = last_pos['lat']
                    longitude = last_pos['lon']
    
    aircraft_dict = {
        "id": aircraft_model.id,
        "created_at": aircraft_model.created_at,
        "updated_at": aircraft_model.last_updated,
        "tenant_id": aircraft_model.tenant_id,
        "hex": aircraft_model.hex,
        "type": aircraft_model.type,
        "flight": aircraft_model.flight,
        "registration": aircraft_model.registration,
        "aircraft_type_code": aircraft_model.aircraft_type_code,
        "db_flags": aircraft_model.db_flags,
        "squawk": aircraft_model.squawk,
        "emergency": aircraft_model.emergency,
        "category": aircraft_model.category,
        "altitude_baro": aircraft_model.altitude_baro,
        "altitude_geom": aircraft_model.altitude_geom,
        "ground_speed": aircraft_model.ground_speed,
        "track": aircraft_model.track,
        "true_heading": aircraft_model.true_heading,
        "vertical_rate": aircraft_model.vertical_rate,
        "nic": aircraft_model.nic,
        "nac_p": aircraft_model.nac_p,
        "nac_v": aircraft_model.nac_v,
        "sil": aircraft_model.sil,
        "sil_type": aircraft_model.sil_type,
        "sda": aircraft_model.sda,
        "messages": aircraft_model.messages,
        "seen": aircraft_model.seen,
        "seen_pos": aircraft_model.seen_pos,
        "rssi": aircraft_model.rssi,
        "gps_ok_before": aircraft_model.gps_ok_before,
        "gps_ok_lat": aircraft_model.gps_ok_lat,
        "gps_ok_lon": aircraft_model.gps_ok_lon,
        "raw_data": aircraft_model.raw_data,
        "latitude": float(latitude) if latitude is not None else None,
        "longitude": float(longitude) if longitude is not None else None,
    }
    
    return Aircraft(**aircraft_dict)


@router.post("/", response_model=Aircraft)
async def create_aircraft(
    aircraft: AircraftCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create new aircraft"""
    tenant = await get_default_tenant(session)
    
    service = AircraftService(session)
    aircraft_model = await service.create_aircraft(tenant.id, aircraft)
    
    # Convert to response format
    aircraft_dict = {
        "id": aircraft_model.id,
        "created_at": aircraft_model.created_at,
        "updated_at": aircraft_model.updated_at,
        "tenant_id": aircraft_model.tenant_id,
        "hex": aircraft_model.hex,
        "type": aircraft_model.type,
        "flight": aircraft_model.flight,
        "registration": aircraft_model.registration,
        "aircraft_type_code": aircraft_model.aircraft_type_code,
        "db_flags": aircraft_model.db_flags,
        "squawk": aircraft_model.squawk,
        "emergency": aircraft_model.emergency,
        "category": aircraft_model.category,
        "altitude_baro": aircraft_model.altitude_baro,
        "altitude_geom": aircraft_model.altitude_geom,
        "ground_speed": aircraft_model.ground_speed,
        "track": aircraft_model.track,
        "true_heading": aircraft_model.true_heading,
        "vertical_rate": aircraft_model.vertical_rate,
        "nic": aircraft_model.nic,
        "nac_p": aircraft_model.nac_p,
        "nac_v": aircraft_model.nac_v,
        "sil": aircraft_model.sil,
        "sil_type": aircraft_model.sil_type,
        "sda": aircraft_model.sda,
        "messages": aircraft_model.messages,
        "seen": aircraft_model.seen,
        "seen_pos": aircraft_model.seen_pos,
        "rssi": aircraft_model.rssi,
        "gps_ok_before": aircraft_model.gps_ok_before,
        "gps_ok_lat": aircraft_model.gps_ok_lat,
        "gps_ok_lon": aircraft_model.gps_ok_lon,
        "raw_data": aircraft_model.raw_data,
        "latitude": aircraft.latitude,
        "longitude": aircraft.longitude,
    }
    
    return Aircraft(**aircraft_dict)


@router.get("/geojson/all")
async def get_aircraft_geojson(
    session: AsyncSession = Depends(get_async_session),
):
    """Get all aircraft as GeoJSON FeatureCollection"""
    tenant = await get_default_tenant(session)
    
    service = AircraftService(session)
    geojson = await service.get_aircraft_geojson(tenant.id)
    
    return geojson


@router.post("/bulk")
async def create_bulk_aircraft(
    aircraft_list: List[dict],
    session: AsyncSession = Depends(get_async_session),
):
    """Bulk create/update aircraft from raw data (for testing)"""
    tenant = await get_default_tenant(session)
    
    service = AircraftService(session)
    result = await service.process_bulk_aircraft_data(tenant.id, aircraft_list)
    
    return {
        "processed": len(aircraft_list),
        "created": result["created"],
        "updated": result["updated"],
        "errors": result["errors"]
    }
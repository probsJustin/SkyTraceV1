"""
Aircraft service for business logic
"""
from typing import Dict, List, Optional, Any
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, update, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from geoalchemy2.functions import ST_Point, ST_GeomFromText
import structlog

from app.models.aircraft import Aircraft as AircraftModel
from app.models.aircraft_archive import AircraftArchive as AircraftArchiveModel
from app.schemas.aircraft import AircraftCreate, AircraftUpdate
from app.utils.validation import validate_aircraft_numeric_fields, safe_aircraft_insert

logger = structlog.get_logger()


class AircraftService:
    """Service class for aircraft operations"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_aircraft(self, tenant_id: UUID, aircraft_data: AircraftCreate) -> AircraftModel:
        """Create new aircraft"""
        aircraft_dict = aircraft_data.model_dump(exclude_unset=True)
        aircraft_dict["tenant_id"] = tenant_id
        
        # Handle position
        latitude = aircraft_dict.pop("latitude", None)
        longitude = aircraft_dict.pop("longitude", None)
        
        if latitude is not None and longitude is not None:
            aircraft_dict["position"] = ST_GeomFromText(f"POINT({longitude} {latitude})", 4326)
        
        # Validate and convert numeric fields using utility function
        aircraft_dict = validate_aircraft_numeric_fields(aircraft_dict)
        
        # Use no_autoflush for safer insertion
        with self.session.no_autoflush:
            aircraft = AircraftModel(**aircraft_dict)
            self.session.add(aircraft)
        
        await self.session.commit()
        await self.session.refresh(aircraft)
        
        logger.info("Aircraft created", aircraft_id=aircraft.id, hex=aircraft.hex)
        return aircraft
    
    async def update_aircraft(self, aircraft_id: UUID, aircraft_data: AircraftUpdate) -> Optional[AircraftModel]:
        """Update existing aircraft"""
        aircraft_dict = aircraft_data.model_dump(exclude_unset=True)
        
        # Handle position
        latitude = aircraft_dict.pop("latitude", None)
        longitude = aircraft_dict.pop("longitude", None)
        
        if latitude is not None and longitude is not None:
            aircraft_dict["position"] = ST_GeomFromText(f"POINT({longitude} {latitude})", 4326)
        
        # Validate and convert numeric fields using utility function
        aircraft_dict = validate_aircraft_numeric_fields(aircraft_dict)
        aircraft_dict["last_updated"] = datetime.utcnow()
        
        # Use no_autoflush for safer update
        with self.session.no_autoflush:
            await self.session.execute(
                update(AircraftModel)
                .where(AircraftModel.id == aircraft_id)
                .values(**aircraft_dict)
            )
        
        await self.session.commit()
        
        result = await self.session.execute(
            select(AircraftModel).where(AircraftModel.id == aircraft_id)
        )
        return result.scalar_one_or_none()
    
    async def get_aircraft_geojson(self, tenant_id: UUID) -> Dict[str, Any]:
        """Get aircraft data as GeoJSON FeatureCollection"""
        query = select(AircraftModel).where(AircraftModel.tenant_id == tenant_id)
        result = await self.session.execute(query)
        aircraft_list = result.scalars().all()
        
        features = []
        for aircraft in aircraft_list:
            if aircraft.position:
                # Extract coordinates - for now we'll parse from the database
                try:
                    # This is a simplified approach - in production you'd use proper PostGIS functions
                    coordinates = [0, 0]  # Default coordinates
                    
                    # Create feature
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": coordinates
                        },
                        "properties": {
                            "id": str(aircraft.id),
                            "hex": aircraft.hex,
                            "flight": aircraft.flight,
                            "registration": aircraft.registration,
                            "aircraft_type": aircraft.aircraft_type_code,
                            "altitude": aircraft.altitude_baro,
                            "speed": aircraft.ground_speed,
                            "track": aircraft.track,
                            "squawk": aircraft.squawk,
                            "emergency": aircraft.emergency,
                            "category": aircraft.category
                        }
                    }
                    features.append(feature)
                except Exception as e:
                    logger.warning("Failed to process aircraft for GeoJSON", 
                                 aircraft_id=aircraft.id, error=str(e))
        
        return {
            "type": "FeatureCollection",
            "features": features
        }
    
    async def process_bulk_aircraft_data(self, tenant_id: UUID, aircraft_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Process bulk aircraft data from external sources"""
        created_count = 0
        updated_count = 0
        error_count = 0
        
        for data in aircraft_data:
            try:
                hex_code = data.get("hex")
                if not hex_code:
                    error_count += 1
                    continue
                
                # Check if aircraft exists
                result = await self.session.execute(
                    select(AircraftModel).where(
                        AircraftModel.tenant_id == tenant_id,
                        AircraftModel.hex == hex_code
                    )
                )
                existing_aircraft = result.scalar_one_or_none()
                
                # Prepare aircraft data
                aircraft_dict = {
                    "tenant_id": tenant_id,
                    "hex": hex_code,
                    "type": data.get("type", "adsb_icao"),
                    "flight": data.get("flight", "").strip() if data.get("flight") else None,
                    "registration": data.get("r"),
                    "aircraft_type_code": data.get("t"),
                    "db_flags": data.get("dbFlags"),
                    "squawk": data.get("squawk"),
                    "emergency": data.get("emergency", "none"),
                    "category": data.get("category"),
                    "altitude_baro": data.get("alt_baro") if data.get("alt_baro") != "ground" else 0,
                    "altitude_geom": data.get("alt_geom"),
                    "ground_speed": data.get("gs"),
                    "track": data.get("track"),
                    "true_heading": data.get("true_heading"),
                    "vertical_rate": data.get("geom_rate"),
                    "nic": data.get("nic"),
                    "nac_p": data.get("nac_p"),
                    "nac_v": data.get("nac_v"),
                    "sil": data.get("sil"),
                    "sil_type": data.get("sil_type"),
                    "sda": data.get("sda"),
                    "messages": data.get("messages"),
                    "seen": data.get("seen"),
                    "seen_pos": data.get("seen_pos"),
                    "rssi": data.get("rssi"),
                    "gps_ok_before": data.get("gpsOkBefore"),
                    "gps_ok_lat": data.get("gpsOkLat"),
                    "gps_ok_lon": data.get("gpsOkLon"),
                    "raw_data": data
                }
                
                # Validate and convert numeric fields
                aircraft_dict = validate_aircraft_numeric_fields(aircraft_dict)
                
                # Handle position
                lat = data.get("lat")
                lon = data.get("lon")
                if lat is not None and lon is not None:
                    aircraft_dict["position"] = ST_GeomFromText(f"POINT({lon} {lat})", 4326)
                elif data.get("lastPosition"):
                    last_pos = data["lastPosition"]
                    if last_pos.get("lat") and last_pos.get("lon"):
                        aircraft_dict["position"] = ST_GeomFromText(f"POINT({last_pos['lon']} {last_pos['lat']})", 4326)
                
                # Use no_autoflush for safer bulk operations
                with self.session.no_autoflush:
                    if existing_aircraft:
                        # Update existing aircraft
                        await self.session.execute(
                            update(AircraftModel)
                            .where(AircraftModel.id == existing_aircraft.id)
                            .values(**{k: v for k, v in aircraft_dict.items() if k != "tenant_id"})
                        )
                        updated_count += 1
                    else:
                        # Create new aircraft
                        new_aircraft = AircraftModel(**aircraft_dict)
                        self.session.add(new_aircraft)
                        created_count += 1
                
            except Exception as e:
                logger.error("Error processing aircraft data", 
                           hex=data.get("hex"), error=str(e))
                error_count += 1
        
        await self.session.commit()
        
        logger.info("Bulk aircraft processing completed",
                   created=created_count, updated=updated_count, errors=error_count)
        
        return {
            "created": created_count,
            "updated": updated_count,
            "errors": error_count
        }
    
    async def archive_and_refresh_aircraft_data(self, tenant_id: UUID, new_aircraft_data: List[Dict[str, Any]], archive_reason: str = "scheduled_refresh") -> Dict[str, int]:
        """
        Archive all current aircraft data and replace with fresh data.
        
        Args:
            tenant_id: UUID of the tenant
            new_aircraft_data: List of new aircraft data to insert
            archive_reason: Reason for archiving (default: 'scheduled_refresh')
            
        Returns:
            Dictionary with counts of archived and created records
        """
        archived_count = 0
        created_count = 0
        error_count = 0
        
        try:
            # Step 1: Archive all existing aircraft for this tenant
            existing_aircraft_query = select(AircraftModel).where(AircraftModel.tenant_id == tenant_id)
            existing_result = await self.session.execute(existing_aircraft_query)
            existing_aircraft = existing_result.scalars().all()
            
            logger.info(f"Archiving {len(existing_aircraft)} aircraft records", tenant_id=tenant_id)
            
            # Archive each existing aircraft record
            for aircraft in existing_aircraft:
                try:
                    archive_record = AircraftArchiveModel(
                        original_aircraft_id=aircraft.id,
                        tenant_id=aircraft.tenant_id,
                        hex=aircraft.hex,
                        type=aircraft.type,
                        flight=aircraft.flight,
                        registration=aircraft.registration,
                        aircraft_type_code=aircraft.aircraft_type_code,
                        db_flags=aircraft.db_flags,
                        squawk=aircraft.squawk,
                        emergency=aircraft.emergency,
                        category=aircraft.category,
                        position=aircraft.position,
                        altitude_baro=aircraft.altitude_baro,
                        altitude_geom=aircraft.altitude_geom,
                        ground_speed=aircraft.ground_speed,
                        track=aircraft.track,
                        true_heading=aircraft.true_heading,
                        vertical_rate=aircraft.vertical_rate,
                        nic=aircraft.nic,
                        nac_p=aircraft.nac_p,
                        nac_v=aircraft.nac_v,
                        sil=aircraft.sil,
                        sil_type=aircraft.sil_type,
                        sda=aircraft.sda,
                        messages=aircraft.messages,
                        seen=aircraft.seen,
                        seen_pos=aircraft.seen_pos,
                        rssi=aircraft.rssi,
                        gps_ok_before=aircraft.gps_ok_before,
                        gps_ok_lat=aircraft.gps_ok_lat,
                        gps_ok_lon=aircraft.gps_ok_lon,
                        raw_data=aircraft.raw_data,
                        original_created_at=aircraft.created_at,
                        original_last_updated=aircraft.last_updated,
                        archive_reason=archive_reason
                    )
                    
                    self.session.add(archive_record)
                    archived_count += 1
                    
                except Exception as e:
                    logger.error(f"Error archiving aircraft {aircraft.id}: {e}")
                    error_count += 1
            
            # Step 2: Delete all existing aircraft for this tenant
            await self.session.execute(
                update(AircraftModel)
                .where(AircraftModel.tenant_id == tenant_id)
                .execution_options(synchronize_session=False)
            )
            
            # Actually delete using a delete statement
            from sqlalchemy import delete
            await self.session.execute(
                delete(AircraftModel).where(AircraftModel.tenant_id == tenant_id)
            )
            
            # Step 3: Insert fresh aircraft data
            for data in new_aircraft_data:
                try:
                    hex_code = data.get("hex")
                    if not hex_code:
                        error_count += 1
                        continue
                    
                    # Prepare aircraft data (reuse existing logic)
                    aircraft_dict = {
                        "tenant_id": tenant_id,
                        "hex": hex_code,
                        "type": data.get("type", "adsb_icao"),
                        "flight": data.get("flight", "").strip() if data.get("flight") else None,
                        "registration": data.get("r"),
                        "aircraft_type_code": data.get("t"),
                        "db_flags": data.get("dbFlags"),
                        "squawk": data.get("squawk"),
                        "emergency": data.get("emergency", "none"),
                        "category": data.get("category"),
                        "altitude_baro": data.get("alt_baro") if data.get("alt_baro") != "ground" else 0,
                        "altitude_geom": data.get("alt_geom"),
                        "ground_speed": data.get("gs"),
                        "track": data.get("track"),
                        "true_heading": data.get("true_heading"),
                        "vertical_rate": data.get("geom_rate"),
                        "nic": data.get("nic"),
                        "nac_p": data.get("nac_p"),
                        "nac_v": data.get("nac_v"),
                        "sil": data.get("sil"),
                        "sil_type": data.get("sil_type"),
                        "sda": data.get("sda"),
                        "messages": data.get("messages"),
                        "seen": data.get("seen"),
                        "seen_pos": data.get("seen_pos"),
                        "rssi": data.get("rssi"),
                        "gps_ok_before": data.get("gpsOkBefore"),
                        "gps_ok_lat": data.get("gpsOkLat"),
                        "gps_ok_lon": data.get("gpsOkLon"),
                        "raw_data": data
                    }
                    
                    # Validate and convert numeric fields
                    aircraft_dict = validate_aircraft_numeric_fields(aircraft_dict)
                    
                    # Handle position
                    lat = data.get("lat")
                    lon = data.get("lon")
                    if lat is not None and lon is not None:
                        aircraft_dict["position"] = ST_GeomFromText(f"POINT({lon} {lat})", 4326)
                    elif data.get("lastPosition"):
                        last_pos = data["lastPosition"]
                        if last_pos.get("lat") and last_pos.get("lon"):
                            aircraft_dict["position"] = ST_GeomFromText(f"POINT({last_pos['lon']} {last_pos['lat']})", 4326)
                    
                    # Create new aircraft
                    new_aircraft = AircraftModel(**aircraft_dict)
                    self.session.add(new_aircraft)
                    created_count += 1
                    
                except Exception as e:
                    logger.error("Error creating fresh aircraft data", 
                               hex=data.get("hex"), error=str(e))
                    error_count += 1
            
            # Commit all changes
            await self.session.commit()
            
            logger.info("Archive and refresh completed",
                       tenant_id=tenant_id,
                       archived=archived_count,
                       created=created_count,
                       errors=error_count)
            
            return {
                "archived": archived_count,
                "created": created_count,
                "errors": error_count
            }
            
        except Exception as e:
            logger.error("Error in archive and refresh process", error=str(e))
            await self.session.rollback()
            raise
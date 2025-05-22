"""
ADSBExchange RapidAPI Client
Collects military aircraft data from ADSBExchange via RapidAPI
"""
import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from uuid import UUID

import httpx
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.base_client import BaseDataClient
from app.services.aircraft_service import AircraftService
from app.core.config import settings

logger = structlog.get_logger()


class ADSBExchangeClient(BaseDataClient):
    """Client for ADSBExchange RapidAPI military aircraft data"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.api_key = self.config.get("rapidapi_key", settings.ADSBEXCHANGE_RAPIDAPI_KEY)
        self.base_url = "https://adsbexchange-com1.p.rapidapi.com"
        self.endpoint = self.config.get("endpoint", "/v2/mil/")  # Military aircraft endpoint
        self.timeout = self.config.get("timeout", 30)
        
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'adsbexchange-com1.p.rapidapi.com',
            'User-Agent': 'SkyTrace/1.0'
        }
        
        self.logger = logger.bind(client="ADSBExchangeClient")
    
    async def fetch_data(self) -> List[Dict[str, Any]]:
        """Fetch aircraft data from ADSBExchange RapidAPI"""
        url = f"{self.base_url}{self.endpoint}"
        
        try:
            self.logger.info("Fetching aircraft data from ADSBExchange", url=url)
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                
                data = response.json()
                
                # ADSBExchange returns data in format: {"ac": [...], "ctime": ..., "ptime": ...}
                aircraft_list = data.get("ac", [])
                
                self.logger.info(
                    "Successfully fetched aircraft data",
                    count=len(aircraft_list),
                    response_time=response.elapsed.total_seconds() if response.elapsed else None
                )
                
                return aircraft_list
                
        except httpx.TimeoutException:
            self.logger.error("Request timeout while fetching aircraft data", url=url)
            raise
        except httpx.HTTPStatusError as e:
            self.logger.error(
                "HTTP error while fetching aircraft data",
                status_code=e.response.status_code,
                response_text=e.response.text[:500],
                url=url
            )
            raise
        except json.JSONDecodeError as e:
            self.logger.error("Invalid JSON response from ADSBExchange", error=str(e))
            raise
        except Exception as e:
            self.logger.error("Unexpected error fetching aircraft data", error=str(e))
            raise
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate aircraft data from ADSBExchange"""
        if not isinstance(data, dict):
            return False
        
        # Check for required fields
        hex_code = data.get("hex")
        if not hex_code or not isinstance(hex_code, str):
            return False
        
        # Validate hex code format (6 character hexadecimal)
        if len(hex_code) != 6:
            return False
        
        try:
            int(hex_code, 16)  # Validate it's valid hex
        except ValueError:
            return False
        
        # Check aircraft type
        aircraft_type = data.get("type")
        if not aircraft_type or aircraft_type not in ["adsb_icao", "mode_s", "tisb", "mlat"]:
            return False
        
        # Validate coordinates if present
        lat = data.get("lat")
        lon = data.get("lon")
        if lat is not None and lon is not None:
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                return False
        
        # Validate altitude if present
        alt = data.get("alt_baro")
        if alt is not None and alt != "ground":
            if not isinstance(alt, (int, float)) or alt < -1000 or alt > 60000:
                return False
        
        return True
    
    def transform_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform ADSBExchange data to our internal format"""
        transformed = []
        
        for aircraft in raw_data:
            if not self.validate_data(aircraft):
                continue
            
            # Transform to our internal format
            transformed_aircraft = {
                # Core identification
                "hex": aircraft.get("hex"),
                "type": aircraft.get("type"),
                "flight": aircraft.get("flight", "").strip() if aircraft.get("flight") else None,
                "registration": aircraft.get("r"),
                "aircraft_type_code": aircraft.get("t"),
                
                # Flags and metadata
                "db_flags": aircraft.get("dbFlags"),
                "squawk": aircraft.get("squawk"),
                "emergency": aircraft.get("emergency", "none"),
                "category": aircraft.get("category"),
                
                # Position data
                "latitude": aircraft.get("lat"),
                "longitude": aircraft.get("lon"),
                "altitude_baro": aircraft.get("alt_baro") if aircraft.get("alt_baro") != "ground" else 0,
                "altitude_geom": aircraft.get("alt_geom"),
                
                # Movement data
                "ground_speed": aircraft.get("gs"),
                "track": aircraft.get("track"),
                "true_heading": aircraft.get("true_heading"),
                "vertical_rate": aircraft.get("geom_rate"),
                
                # Quality indicators
                "nic": aircraft.get("nic"),
                "nac_p": aircraft.get("nac_p"),
                "nac_v": aircraft.get("nac_v"),
                "sil": aircraft.get("sil"),
                "sil_type": aircraft.get("sil_type"),
                "sda": aircraft.get("sda"),
                
                # Signal data
                "messages": aircraft.get("messages"),
                "seen": aircraft.get("seen"),
                "seen_pos": aircraft.get("seen_pos"),
                "rssi": aircraft.get("rssi"),
                
                # GPS data for aircraft without current position
                "gps_ok_before": aircraft.get("gpsOkBefore"),
                "gps_ok_lat": aircraft.get("gpsOkLat"),
                "gps_ok_lon": aircraft.get("gpsOkLon"),
                
                # Store raw data for debugging
                "raw_data": aircraft,
                
                # Add collection metadata
                "collected_at": datetime.utcnow().isoformat(),
                "data_source": "adsbexchange_rapidapi"
            }
            
            # Handle lastPosition data for aircraft without current position
            if not transformed_aircraft["latitude"] and aircraft.get("lastPosition"):
                last_pos = aircraft["lastPosition"]
                transformed_aircraft["latitude"] = last_pos.get("lat")
                transformed_aircraft["longitude"] = last_pos.get("lon")
                transformed_aircraft["nic"] = last_pos.get("nic")
                transformed_aircraft["seen_pos"] = last_pos.get("seen_pos")
            
            transformed.append(transformed_aircraft)
        
        return transformed
    
    async def store_data(self, session: AsyncSession, tenant_id: UUID, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Store aircraft data in database"""
        try:
            aircraft_service = AircraftService(session)
            result = await aircraft_service.process_bulk_aircraft_data(tenant_id, data)
            
            self.logger.info(
                "Aircraft data stored successfully",
                aircraft_count=len(data),
                created=result.get("created", 0),
                updated=result.get("updated", 0),
                errors=result.get("errors", 0)
            )
            
            return {
                "created": result.get("created", 0),
                "updated": result.get("updated", 0),
                "errors": result.get("errors", 0)
            }
            
        except Exception as e:
            self.logger.error("Failed to store aircraft data", error=str(e))
            raise
    
    async def archive_and_refresh_data(self, session: AsyncSession, tenant_id: UUID, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Archive current aircraft and refresh with new data"""
        try:
            aircraft_service = AircraftService(session)
            result = await aircraft_service.archive_and_refresh_aircraft_data(
                tenant_id, 
                data, 
                archive_reason="adsb_scheduled_refresh"
            )
            
            self.logger.info(
                "Aircraft data archived and refreshed successfully",
                aircraft_count=len(data),
                archived=result.get("archived", 0),
                created=result.get("created", 0),
                errors=result.get("errors", 0)
            )
            
            return {
                "archived": result.get("archived", 0),
                "created": result.get("created", 0),
                "errors": result.get("errors", 0)
            }
            
        except Exception as e:
            self.logger.error("Failed to archive and refresh aircraft data", error=str(e))
            raise
    
    def get_client_info(self) -> Dict[str, Any]:
        """Get information about this client"""
        return {
            "name": "ADSBExchange RapidAPI Client",
            "version": "1.0.0",
            "data_source": "adsbexchange_rapidapi",
            "endpoint": f"{self.base_url}{self.endpoint}",
            "description": "Collects military aircraft data from ADSBExchange via RapidAPI",
            "update_frequency": "30 minutes",
            "data_type": "aircraft",
            "coverage": "Global military aircraft",
            "fields": [
                "hex", "type", "flight", "registration", "aircraft_type_code",
                "latitude", "longitude", "altitude_baro", "ground_speed",
                "track", "squawk", "emergency", "category"
            ]
        }


# Convenience function for standalone testing
async def test_client():
    """Test the ADSBExchange client"""
    print("🚀 Testing ADSBExchange Client...")
    
    config = {
        "rapidapi_key": settings.ADSBEXCHANGE_RAPIDAPI_KEY,
        "endpoint": "/v2/mil/",
        "timeout": 30
    }
    
    client = ADSBExchangeClient(config)
    
    try:
        data = await client.process_data()
        print(f"✅ Successfully collected {len(data)} aircraft")
        
        if data:
            print("\n📊 Sample aircraft:")
            for i, aircraft in enumerate(data[:3]):  # Show first 3
                print(f"  {i+1}. {aircraft.get('hex')} - {aircraft.get('flight', 'N/A')} ({aircraft.get('aircraft_type_code', 'Unknown')})")
        
        return data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


if __name__ == "__main__":
    asyncio.run(test_client())
"""
Airspace service for fetching restricted airspace data from FAA
"""
import aiohttp
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import ssl
import json

logger = logging.getLogger(__name__)

class AirspaceService:
    """Service for fetching and processing restricted airspace data"""
    
    FAA_AIRSPACE_URL = "https://sua.faa.gov/sua/schedule.json"
    
    def __init__(self):
        self.session = None
    
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            # Create SSL context that's more permissive for FAA endpoint
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Connection': 'keep-alive'
            }
            
            self.session = aiohttp.ClientSession(
                connector=connector,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            )
        
        return self.session
    
    def parse_mbr_to_bbox(self, mbr_string: str) -> Optional[Dict[str, float]]:
        """
        Parse MBR string to bounding box coordinates
        MBR format: "min_x,min_y,max_x,max_y" in Web Mercator projection
        """
        try:
            coords = [float(x) for x in mbr_string.split(',')]
            if len(coords) != 4:
                return None
            
            # Convert from Web Mercator to lat/lng (approximate)
            # This is a simplified conversion - for production you'd want proper projection
            min_x, min_y, max_x, max_y = coords
            
            # Web Mercator to WGS84 conversion (simplified)
            min_lng = min_x / 111319.9
            max_lng = max_x / 111319.9
            min_lat = min_y / 111319.9  
            max_lat = max_y / 111319.9
            
            # Clamp to valid lat/lng ranges
            min_lng = max(-180, min(180, min_lng))
            max_lng = max(-180, min(180, max_lng))
            min_lat = max(-90, min(90, min_lat))
            max_lat = max(-90, min(90, max_lat))
            
            return {
                'min_lng': min_lng,
                'min_lat': min_lat,
                'max_lng': max_lng,
                'max_lat': max_lat
            }
        except (ValueError, IndexError) as e:
            logger.warning(f"Failed to parse MBR: {mbr_string}, error: {e}")
            return None
    
    def get_airspace_color(self, airspace_type: str, type_class: str) -> str:
        """Get color for airspace based on type"""
        color_map = {
            'R': '#FF4444',  # Restricted - Red
            'A': '#FF8800',  # ATCAA - Orange  
            'M': '#FFAA00',  # MOA - Yellow-Orange
            'W': '#AA00FF',  # Warning - Purple
            'P': '#FF0088',  # Prohibited - Pink
            'T': '#0088FF',  # TFR - Blue
        }
        return color_map.get(airspace_type, '#888888')  # Default gray
    
    def process_airspace_record(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single airspace record into GeoJSON feature"""
        try:
            bbox = self.parse_mbr_to_bbox(record.get('mbr', ''))
            if not bbox:
                return None
            
            # Create a rectangle polygon from bounding box
            coordinates = [[
                [bbox['min_lng'], bbox['min_lat']],  # Bottom-left
                [bbox['max_lng'], bbox['min_lat']],  # Bottom-right
                [bbox['max_lng'], bbox['max_lat']],  # Top-right
                [bbox['min_lng'], bbox['max_lat']],  # Top-left
                [bbox['min_lng'], bbox['min_lat']]   # Close polygon
            ]]
            
            airspace_type = record.get('type', 'Unknown')
            color = self.get_airspace_color(airspace_type, record.get('type_class', ''))
            
            # Parse times
            start_time = record.get('start_time', '')
            end_time = record.get('end_time', '')
            
            return {
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': coordinates
                },
                'properties': {
                    'gid': record.get('gid'),
                    'airspace_name': record.get('airspace_name', ''),
                    'type': airspace_type,
                    'type_class': record.get('type_class', ''),
                    'start_time': start_time,
                    'end_time': end_time,
                    'center_id': record.get('CenterID', ''),
                    'state': record.get('state', ''),
                    'min_alt': record.get('min_alt', 0),
                    'max_alt': record.get('max_alt', 0),
                    'agl': record.get('agl', 0),
                    'time_box': record.get('time_box', ''),
                    'is_new': record.get('is_new', ''),
                    'color': color,
                    'opacity': 0.3,
                    'stroke_color': color,
                    'stroke_width': 2
                }
            }
        except Exception as e:
            logger.warning(f"Failed to process airspace record: {e}")
            return None
    
    async def fetch_airspace_data(self, limit: int = 3000) -> Dict[str, Any]:
        """Fetch airspace data from FAA API"""
        try:
            session = await self.get_session()
            
            params = {
                'limit': limit,
                'raw': 'true'
            }
            
            async with session.get(self.FAA_AIRSPACE_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if not data or 'schedule' not in data:
                        logger.error("Invalid response format from FAA API")
                        return {'type': 'FeatureCollection', 'features': []}
                    
                    logger.info(f"Retrieved {len(data['schedule'])} airspace records")
                    
                    # Process records into GeoJSON features
                    features = []
                    for record in data['schedule']:
                        feature = self.process_airspace_record(record)
                        if feature:
                            features.append(feature)
                    
                    logger.info(f"Successfully processed {len(features)} airspace features")
                    
                    return {
                        'type': 'FeatureCollection',
                        'features': features,
                        'total': len(features),
                        'retrieved_at': datetime.utcnow().isoformat()
                    }
                else:
                    logger.error(f"FAA API returned status {response.status}")
                    return {'type': 'FeatureCollection', 'features': []}
                    
        except Exception as e:
            logger.error(f"Failed to fetch airspace data: {e}")
            return {'type': 'FeatureCollection', 'features': []}
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

# Global service instance
airspace_service = AirspaceService()
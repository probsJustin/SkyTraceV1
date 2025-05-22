"""
Mock aircraft client for testing
"""
import random
from typing import Dict, List, Any
from datetime import datetime

from .base_client import BaseDataClient


class MockAircraftClient(BaseDataClient):
    """Mock aircraft client that generates test data"""
    
    async def fetch_data(self) -> List[Dict[str, Any]]:
        """Generate mock aircraft data"""
        mock_aircraft = []
        
        # Generate 10-50 random aircraft
        num_aircraft = random.randint(10, 50)
        
        for i in range(num_aircraft):
            # Random hex code
            hex_code = f"{random.randint(0, 0xFFFFFF):06x}"
            
            # Random position around San Francisco area
            lat = 37.7749 + random.uniform(-0.5, 0.5)
            lon = -122.4194 + random.uniform(-0.5, 0.5)
            
            aircraft = {
                "hex": hex_code,
                "type": random.choice(["adsb_icao", "mode_s"]),
                "flight": f"TEST{random.randint(100, 999)}" if random.random() > 0.3 else None,
                "r": f"N{random.randint(100, 999)}AB" if random.random() > 0.5 else None,
                "t": random.choice(["B738", "A320", "B777", "A350", "C172"]),
                "dbFlags": 1,
                "alt_baro": random.randint(0, 40000) if random.random() > 0.1 else "ground",
                "gs": round(random.uniform(0, 500), 1),
                "track": round(random.uniform(0, 359), 2),
                "true_heading": round(random.uniform(0, 359), 2),
                "squawk": f"{random.randint(1000, 7777):04d}",
                "emergency": "none",
                "category": random.choice(["A1", "A2", "A3", "A4", "A5"]),
                "lat": lat,
                "lon": lon,
                "nic": random.randint(0, 11),
                "rc": random.randint(10, 500),
                "seen_pos": round(random.uniform(0, 30), 2),
                "version": random.choice([0, 1, 2]),
                "nac_p": random.randint(0, 11),
                "nac_v": random.randint(0, 4),
                "sil": random.randint(0, 3),
                "sil_type": random.choice(["perhour", "persample"]),
                "sda": random.randint(0, 3),
                "messages": random.randint(1000, 1000000),
                "seen": round(random.uniform(0, 10), 1),
                "rssi": round(random.uniform(-50, -10), 1),
            }
            
            mock_aircraft.append(aircraft)
        
        return mock_aircraft
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate aircraft data"""
        required_fields = ["hex", "type"]
        
        for field in required_fields:
            if field not in data or data[field] is None:
                return False
        
        # Validate hex code format
        hex_code = data.get("hex", "")
        if not isinstance(hex_code, str) or len(hex_code) != 6:
            return False
        
        # Validate coordinates if present
        lat = data.get("lat")
        lon = data.get("lon")
        if lat is not None and lon is not None:
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                return False
        
        return True
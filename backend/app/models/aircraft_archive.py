"""
Aircraft archive model for storing historical aircraft tracking data
"""
from decimal import Decimal
from sqlalchemy import BigInteger, Column, Enum, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import uuid
from datetime import datetime

from app.core.database import Base


class AircraftArchive(Base):
    """Aircraft archive model for storing historical aircraft tracking data"""
    
    __tablename__ = "aircraft_archive"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_aircraft_id = Column(UUID(as_uuid=True), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    hex = Column(String(6), nullable=False)  # ICAO 24-bit address
    type = Column(Enum("adsb_icao", "mode_s", "tisb", "mlat", name="aircraft_type"), nullable=False)
    flight = Column(String(20))
    registration = Column(String(20))
    aircraft_type_code = Column(String(10))  # Aircraft type (e.g., B738, A320)
    db_flags = Column(Integer)
    squawk = Column(String(4))
    emergency = Column(Enum("none", "general", "lifeguard", "minfuel", "nordo", "unlawful", "downed", 
                           name="emergency_type"), default="none")
    category = Column(String(5))
    
    # Position data
    position = Column(Geometry("POINT", srid=4326))
    altitude_baro = Column(Integer)
    altitude_geom = Column(Integer)
    ground_speed = Column(Numeric(8, 2))
    track = Column(Numeric(6, 2))
    true_heading = Column(Numeric(6, 2))
    vertical_rate = Column(Integer)
    
    # Quality indicators
    nic = Column(Integer)  # Navigation Integrity Category
    nac_p = Column(Integer)  # Navigation Accuracy Category - Position
    nac_v = Column(Integer)  # Navigation Accuracy Category - Velocity
    sil = Column(Integer)  # Source Integrity Level
    sil_type = Column(String(20))
    sda = Column(Integer)  # System Design Assurance
    
    # Timing and signal data
    messages = Column(BigInteger)
    seen = Column(Numeric(10, 2))
    seen_pos = Column(Numeric(10, 2))
    rssi = Column(Numeric(6, 2))
    
    # GPS data
    gps_ok_before = Column(Numeric(15, 1))
    gps_ok_lat = Column(Numeric(10, 6))
    gps_ok_lon = Column(Numeric(11, 6))
    
    # Raw data
    raw_data = Column(JSONB)
    
    # Archive-specific fields
    archived_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    original_created_at = Column(DateTime)
    original_last_updated = Column(DateTime)
    archive_reason = Column(String(50), default="scheduled_refresh")
    
    # Relationships
    tenant = relationship("Tenant")
    
    def __repr__(self) -> str:
        return f"<AircraftArchive(id={self.id}, hex='{self.hex}', archived_at='{self.archived_at}')>"
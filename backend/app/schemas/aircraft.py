"""
Aircraft Pydantic schemas
"""
from typing import Any, Dict, List, Optional
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema


class AircraftPosition(BaseModel):
    """Aircraft position schema"""
    latitude: float
    longitude: float


class AircraftCreate(BaseCreateSchema):
    """Schema for creating aircraft"""
    hex: str = Field(..., min_length=6, max_length=6, description="ICAO 24-bit address")
    type: str = Field(..., description="Aircraft type (adsb_icao, mode_s, tisb, mlat)")
    flight: Optional[str] = Field(None, max_length=20, description="Flight number")
    registration: Optional[str] = Field(None, max_length=20, description="Aircraft registration")
    aircraft_type_code: Optional[str] = Field(None, max_length=10, description="Aircraft type code")
    db_flags: Optional[int] = None
    squawk: Optional[str] = Field(None, max_length=4, description="Squawk code")
    emergency: Optional[str] = Field("none", description="Emergency status")
    category: Optional[str] = Field(None, max_length=5, description="Aircraft category")
    
    # Position data
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude")
    altitude_baro: Optional[int] = Field(None, description="Barometric altitude")
    altitude_geom: Optional[int] = Field(None, description="Geometric altitude")
    ground_speed: Optional[float] = Field(None, ge=0, description="Ground speed")
    track: Optional[float] = Field(None, ge=0, lt=360, description="Track direction")
    true_heading: Optional[float] = Field(None, ge=0, lt=360, description="True heading")
    vertical_rate: Optional[int] = Field(None, description="Vertical rate")
    
    # Quality indicators
    nic: Optional[int] = Field(None, description="Navigation Integrity Category")
    nac_p: Optional[int] = Field(None, description="Navigation Accuracy Category - Position")
    nac_v: Optional[int] = Field(None, description="Navigation Accuracy Category - Velocity")
    sil: Optional[int] = Field(None, description="Source Integrity Level")
    sil_type: Optional[str] = Field(None, description="SIL type")
    sda: Optional[int] = Field(None, description="System Design Assurance")
    
    # Timing and signal data
    messages: Optional[int] = Field(None, description="Number of messages")
    seen: Optional[float] = Field(None, description="Time since last message")
    seen_pos: Optional[float] = Field(None, description="Time since last position")
    rssi: Optional[float] = Field(None, description="Signal strength")
    
    # GPS data
    gps_ok_before: Optional[float] = None
    gps_ok_lat: Optional[float] = None
    gps_ok_lon: Optional[float] = None
    
    # Raw data
    raw_data: Optional[Dict[str, Any]] = Field(None, description="Raw aircraft data")


class AircraftUpdate(BaseUpdateSchema):
    """Schema for updating aircraft"""
    flight: Optional[str] = Field(None, max_length=20)
    registration: Optional[str] = Field(None, max_length=20)
    aircraft_type_code: Optional[str] = Field(None, max_length=10)
    db_flags: Optional[int] = None
    squawk: Optional[str] = Field(None, max_length=4)
    emergency: Optional[str] = None
    category: Optional[str] = Field(None, max_length=5)
    
    # Position data
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    altitude_baro: Optional[int] = None
    altitude_geom: Optional[int] = None
    ground_speed: Optional[float] = Field(None, ge=0)
    track: Optional[float] = Field(None, ge=0, lt=360)
    true_heading: Optional[float] = Field(None, ge=0, lt=360)
    vertical_rate: Optional[int] = None
    
    # Quality indicators
    nic: Optional[int] = None
    nac_p: Optional[int] = None
    nac_v: Optional[int] = None
    sil: Optional[int] = None
    sil_type: Optional[str] = None
    sda: Optional[int] = None
    
    # Timing and signal data
    messages: Optional[int] = None
    seen: Optional[float] = None
    seen_pos: Optional[float] = None
    rssi: Optional[float] = None
    
    # GPS data
    gps_ok_before: Optional[float] = None
    gps_ok_lat: Optional[float] = None
    gps_ok_lon: Optional[float] = None
    
    # Raw data
    raw_data: Optional[Dict[str, Any]] = None


class Aircraft(BaseSchema):
    """Aircraft response schema"""
    tenant_id: UUID
    hex: str
    type: str
    flight: Optional[str] = None
    registration: Optional[str] = None
    aircraft_type_code: Optional[str] = None
    db_flags: Optional[int] = None
    squawk: Optional[str] = None
    emergency: Optional[str] = None
    category: Optional[str] = None
    
    # Position data (computed from geometry)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude_baro: Optional[int] = None
    altitude_geom: Optional[int] = None
    ground_speed: Optional[float] = None
    track: Optional[float] = None
    true_heading: Optional[float] = None
    vertical_rate: Optional[int] = None
    
    # Quality indicators
    nic: Optional[int] = None
    nac_p: Optional[int] = None
    nac_v: Optional[int] = None
    sil: Optional[int] = None
    sil_type: Optional[str] = None
    sda: Optional[int] = None
    
    # Timing and signal data
    messages: Optional[int] = None
    seen: Optional[float] = None
    seen_pos: Optional[float] = None
    rssi: Optional[float] = None
    
    # GPS data
    gps_ok_before: Optional[float] = None
    gps_ok_lat: Optional[float] = None
    gps_ok_lon: Optional[float] = None
    
    # Raw data
    raw_data: Optional[Dict[str, Any]] = None


class AircraftResponse(BaseModel):
    """Aircraft API response schema"""
    aircraft: List[Aircraft]
    total: int
    page: int
    size: int
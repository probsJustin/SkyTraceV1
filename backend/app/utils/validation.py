"""
Data validation utilities for aircraft data processing
"""
from typing import Any, Dict, Optional, Union, Type
from decimal import Decimal, InvalidOperation
import structlog

logger = structlog.get_logger()


def safe_numeric_convert(
    value: Any, 
    target_type: Type[Union[int, float, Decimal]], 
    field_name: str = "unknown"
) -> Optional[Union[int, float, Decimal]]:
    """
    Safely convert a value to numeric type with proper error handling.
    
    Args:
        value: The value to convert
        target_type: Target numeric type (int, float, or Decimal)
        field_name: Field name for logging purposes
        
    Returns:
        Converted numeric value or None if conversion fails
    """
    if value is None or value == "":
        return None
    
    # If already the correct type, return as-is
    if isinstance(value, target_type):
        return value
    
    try:
        # Handle string conversion
        if isinstance(value, str):
            # Remove whitespace and handle empty strings
            value = value.strip()
            if not value:
                return None
            
            # Handle special cases
            if value.lower() in ('null', 'none', 'n/a', 'na'):
                return None
        
        # Convert to target type
        if target_type == Decimal:
            return Decimal(str(value))
        else:
            return target_type(value)
            
    except (ValueError, TypeError, InvalidOperation) as e:
        logger.warning(
            "Failed to convert field to numeric type",
            field=field_name,
            value=value,
            target_type=target_type.__name__,
            error=str(e)
        )
        return None


def validate_aircraft_numeric_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and convert numeric fields in aircraft data.
    
    Args:
        data: Dictionary containing aircraft data
        
    Returns:
        Dictionary with validated and converted numeric fields
    """
    # Define field type mappings based on database schema
    numeric_field_types = {
        # Position and movement data
        "ground_speed": float,      # DECIMAL(8,2) 
        "track": float,             # DECIMAL(6,2)
        "true_heading": float,      # DECIMAL(6,2)
        
        # Timing and signal data
        "seen": float,              # DECIMAL(10,2)
        "seen_pos": float,          # DECIMAL(10,2) 
        "rssi": float,              # DECIMAL(6,2)
        
        # GPS data
        "gps_ok_before": float,     # DECIMAL(15,1)
        "gps_ok_lat": float,        # DECIMAL(10,6)
        "gps_ok_lon": float,        # DECIMAL(11,6)
        
        # Integer fields
        "altitude_baro": int,
        "altitude_geom": int,
        "vertical_rate": int,
        "nic": int,
        "nac_p": int,
        "nac_v": int,
        "sil": int,
        "sda": int,
        "messages": int,
        "db_flags": int,
        
        # Coordinate fields
        "latitude": float,
        "longitude": float,
    }
    
    validated_data = data.copy()
    
    for field_name, target_type in numeric_field_types.items():
        if field_name in validated_data:
            validated_data[field_name] = safe_numeric_convert(
                validated_data[field_name], 
                target_type, 
                field_name
            )
    
    return validated_data


async def safe_aircraft_insert(session, aircraft_model_class, **kwargs):
    """
    Safely insert aircraft data with automatic numeric validation.
    
    Args:
        session: SQLAlchemy async session
        aircraft_model_class: Aircraft model class
        **kwargs: Aircraft data fields
        
    Returns:
        Created aircraft model instance
    """
    # Validate numeric fields
    validated_data = validate_aircraft_numeric_fields(kwargs)
    
    # Use no_autoflush to prevent premature commits
    with session.no_autoflush:
        aircraft = aircraft_model_class(**validated_data)
        session.add(aircraft)
    
    return aircraft


async def safe_aircraft_update(session, aircraft_instance, **update_data):
    """
    Safely update aircraft data with automatic numeric validation.
    
    Args:
        session: SQLAlchemy async session  
        aircraft_instance: Existing aircraft model instance
        **update_data: Fields to update
        
    Returns:
        Updated aircraft model instance
    """
    # Validate numeric fields
    validated_data = validate_aircraft_numeric_fields(update_data)
    
    # Use no_autoflush to prevent premature commits
    with session.no_autoflush:
        for field, value in validated_data.items():
            if hasattr(aircraft_instance, field):
                setattr(aircraft_instance, field, value)
    
    return aircraft_instance
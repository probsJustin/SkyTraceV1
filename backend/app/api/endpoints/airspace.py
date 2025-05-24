"""
Airspace API endpoints
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query
import structlog

from app.services.airspace_service import airspace_service

logger = structlog.get_logger()
router = APIRouter()


@router.get("/geojson", response_model=Dict[str, Any])
async def get_airspace_geojson(
    limit: int = Query(default=3000, ge=1, le=5000, description="Maximum number of airspace records to fetch")
):
    """
    Get restricted airspace data as GeoJSON
    
    Returns active and scheduled restricted airspace from the FAA including:
    - Restricted areas (R)
    - Military Operating Areas (MOA) 
    - Air Traffic Control Assigned Airspace (ATCAA)
    - Warning areas (W)
    - Prohibited areas (P)
    - Temporary Flight Restrictions (TFR)
    """
    try:
        logger.info("Fetching airspace data", limit=limit)
        
        airspace_data = await airspace_service.fetch_airspace_data(limit=limit)
        
        logger.info(
            "Successfully retrieved airspace data",
            features_count=len(airspace_data.get('features', [])),
            total=airspace_data.get('total', 0)
        )
        
        return airspace_data
        
    except Exception as e:
        logger.error("Failed to fetch airspace data", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch airspace data: {str(e)}"
        )


@router.get("/types")
async def get_airspace_types():
    """
    Get information about airspace types and their meanings
    """
    return {
        "types": {
            "R": {
                "name": "Restricted Area",
                "description": "Airspace with activities hazardous to flight",
                "color": "#FF4444"
            },
            "A": {
                "name": "ATCAA", 
                "description": "Air Traffic Control Assigned Airspace",
                "color": "#FF8800"
            },
            "M": {
                "name": "MOA",
                "description": "Military Operating Area", 
                "color": "#FFAA00"
            },
            "W": {
                "name": "Warning Area",
                "description": "Airspace with potentially hazardous activities",
                "color": "#AA00FF"
            },
            "P": {
                "name": "Prohibited Area",
                "description": "Airspace where flight is prohibited",
                "color": "#FF0088"
            },
            "T": {
                "name": "TFR",
                "description": "Temporary Flight Restriction",
                "color": "#0088FF"
            }
        }
    }
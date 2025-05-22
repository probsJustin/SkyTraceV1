"""
Base client class for data collection
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from uuid import UUID
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger()


class BaseDataClient(ABC):
    """Base class for all data collection clients"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logger.bind(client=self.__class__.__name__)
    
    @abstractmethod
    async def fetch_data(self) -> List[Dict[str, Any]]:
        """Fetch data from the source"""
        pass
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate a single data record"""
        pass
    
    @abstractmethod
    def transform_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform raw data to internal format"""
        pass
    
    @abstractmethod
    async def store_data(self, session: AsyncSession, tenant_id: UUID, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Store processed data in database. Returns stats dict with counts."""
        pass
    
    async def process_data(self) -> List[Dict[str, Any]]:
        """Process and validate fetched data"""
        try:
            raw_data = await self.fetch_data()
            transformed_data = self.transform_data(raw_data)
            validated_data = []
            
            for record in transformed_data:
                if self.validate_data(record):
                    validated_data.append(record)
                else:
                    self.logger.warning("Invalid data record", record=record)
            
            self.logger.info("Data processing completed", 
                           total=len(raw_data), 
                           transformed=len(transformed_data),
                           validated=len(validated_data))
            
            return validated_data
            
        except Exception as e:
            self.logger.error("Error processing data", error=str(e))
            raise
    
    async def fetch_and_store_data(self, session: AsyncSession, tenant_id: UUID, use_archive_refresh: bool = False) -> Dict[str, Any]:
        """Complete workflow: fetch, process, and store data"""
        try:
            # Process data
            processed_data = await self.process_data()
            
            # Store in database
            if processed_data:
                if use_archive_refresh:
                    storage_result = await self.archive_and_refresh_data(session, tenant_id, processed_data)
                else:
                    storage_result = await self.store_data(session, tenant_id, processed_data)
                
                self.logger.info(
                    "Data collection and storage completed",
                    collected=len(processed_data),
                    archive_refresh=use_archive_refresh,
                    **storage_result
                )
                
                return {
                    "success": True,
                    "collected": len(processed_data),
                    **storage_result
                }
            else:
                self.logger.warning("No data collected")
                return {
                    "success": True,
                    "collected": 0,
                    "created": 0,
                    "updated": 0,
                    "errors": 0
                }
                
        except Exception as e:
            self.logger.error("Error in fetch and store workflow", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "collected": 0,
                "created": 0,
                "updated": 0,
                "errors": 1
            }
    
    async def archive_and_refresh_data(self, session: AsyncSession, tenant_id: UUID, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Archive current data and refresh with new data.
        Default implementation - subclasses can override for specific behavior.
        """
        # This method should be implemented by specific client types
        # For aircraft clients, this will use AircraftService.archive_and_refresh_aircraft_data
        # For other data types, implement similar logic
        raise NotImplementedError("Subclasses must implement archive_and_refresh_data method")
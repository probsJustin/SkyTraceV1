"""
Data Source Pydantic schemas
"""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import Field

from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema


class DataSourceCreate(BaseCreateSchema):
    """Schema for creating data sources"""
    name: str = Field(..., min_length=1, max_length=255, description="Data source name")
    type: str = Field(..., min_length=1, max_length=100, description="Data source type")
    client_class: str = Field(..., min_length=1, max_length=255, description="Python client class")
    config: Optional[Dict[str, Any]] = Field(None, description="Client configuration")
    is_active: bool = Field(True, description="Whether data source is active")
    refresh_interval: int = Field(60, ge=1, description="Refresh interval in seconds")


class DataSourceUpdate(BaseUpdateSchema):
    """Schema for updating data sources"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[str] = Field(None, min_length=1, max_length=100)
    client_class: Optional[str] = Field(None, min_length=1, max_length=255)
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    refresh_interval: Optional[int] = Field(None, ge=1)


class DataSource(BaseSchema):
    """Data source response schema"""
    tenant_id: UUID
    name: str
    type: str
    client_class: str
    config: Optional[Dict[str, Any]] = None
    is_active: bool
    refresh_interval: int
    last_updated: Optional[datetime] = None


class DataSourceResponse(BaseSchema):
    """Single data source response"""
    pass
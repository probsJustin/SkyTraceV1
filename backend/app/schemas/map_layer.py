"""
Map Layer Pydantic schemas
"""
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import Field

from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema


class MapLayerCreate(BaseCreateSchema):
    """Schema for creating map layers"""
    name: str = Field(..., min_length=1, max_length=255, description="Layer name")
    description: Optional[str] = Field(None, description="Layer description")
    layer_type: str = Field(..., min_length=1, max_length=100, description="Layer type")
    data_source_id: Optional[UUID] = Field(None, description="Associated data source")
    style_config: Optional[Dict[str, Any]] = Field(None, description="Layer styling configuration")
    is_visible: bool = Field(True, description="Whether layer is visible")
    is_active: bool = Field(True, description="Whether layer is active")
    z_index: int = Field(0, description="Layer z-index for ordering")


class MapLayerUpdate(BaseUpdateSchema):
    """Schema for updating map layers"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    layer_type: Optional[str] = Field(None, min_length=1, max_length=100)
    data_source_id: Optional[UUID] = None
    style_config: Optional[Dict[str, Any]] = None
    is_visible: Optional[bool] = None
    is_active: Optional[bool] = None
    z_index: Optional[int] = None


class MapLayer(BaseSchema):
    """Map layer response schema"""
    tenant_id: UUID
    name: str
    description: Optional[str] = None
    layer_type: str
    data_source_id: Optional[UUID] = None
    style_config: Optional[Dict[str, Any]] = None
    is_visible: bool
    is_active: bool
    z_index: int


class MapLayerResponse(BaseSchema):
    """Single map layer response"""
    pass
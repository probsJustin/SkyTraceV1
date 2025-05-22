"""
Feature Flag Pydantic schemas
"""
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema


class FeatureFlagCreate(BaseCreateSchema):
    """Schema for creating feature flags"""
    name: str = Field(..., min_length=1, max_length=100, description="Feature flag name")
    enabled: bool = Field(False, description="Whether feature is enabled")
    description: Optional[str] = Field(None, description="Feature description")


class FeatureFlagUpdate(BaseUpdateSchema):
    """Schema for updating feature flags"""
    enabled: Optional[bool] = None
    description: Optional[str] = None


class FeatureFlag(BaseSchema):
    """Feature flag response schema"""
    tenant_id: UUID
    name: str
    enabled: bool
    description: Optional[str] = None


class FeatureFlagResponse(BaseSchema):
    """Single feature flag response"""
    pass
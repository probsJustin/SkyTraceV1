"""
Tenant Pydantic schemas
"""
from typing import Optional

from pydantic import Field

from .base import BaseSchema, BaseCreateSchema, BaseUpdateSchema


class TenantCreate(BaseCreateSchema):
    """Schema for creating tenants"""
    name: str = Field(..., min_length=1, max_length=255, description="Tenant name")
    slug: str = Field(..., min_length=1, max_length=100, description="Tenant slug")
    is_active: bool = Field(True, description="Whether tenant is active")


class TenantUpdate(BaseUpdateSchema):
    """Schema for updating tenants"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None


class Tenant(BaseSchema):
    """Tenant response schema"""
    name: str
    slug: str
    is_active: bool


class TenantResponse(BaseSchema):
    """Single tenant response"""
    pass
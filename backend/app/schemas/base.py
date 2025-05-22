"""
Base Pydantic schemas
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common fields"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime


class BaseCreateSchema(BaseModel):
    """Base schema for create operations"""
    model_config = ConfigDict(from_attributes=True)


class BaseUpdateSchema(BaseModel):
    """Base schema for update operations"""
    model_config = ConfigDict(from_attributes=True)
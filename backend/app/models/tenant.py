"""
Tenant model for multi-tenancy support
"""
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base


class Tenant(Base):
    """Tenant model for multi-tenant architecture"""
    
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    feature_flags = relationship("FeatureFlag", back_populates="tenant", cascade="all, delete-orphan")
    data_sources = relationship("DataSource", back_populates="tenant", cascade="all, delete-orphan")
    aircraft = relationship("Aircraft", back_populates="tenant", cascade="all, delete-orphan")
    map_layers = relationship("MapLayer", back_populates="tenant", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Tenant(id={self.id}, name='{self.name}', slug='{self.slug}')>"
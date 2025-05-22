"""
Data source model for managing different data clients
"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base


class DataSource(Base):
    """Data source model for managing different data collection clients"""
    
    __tablename__ = "data_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)  # 'aircraft', 'ships', 'locations', etc.
    client_class = Column(String(255), nullable=False)  # Python class name
    config = Column(JSONB)  # Configuration for the client
    is_active = Column(Boolean, default=True, nullable=False)
    refresh_interval = Column(Integer, default=60)  # seconds
    last_updated = Column(DateTime)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="data_sources")
    map_layers = relationship("MapLayer", back_populates="data_source")
    
    def __repr__(self) -> str:
        return f"<DataSource(id={self.id}, name='{self.name}', type='{self.type}')>"
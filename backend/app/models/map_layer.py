"""
Map layer model for managing map layers and visualizations
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base


class MapLayer(Base):
    """Map layer model for managing different map layers"""
    
    __tablename__ = "map_layers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    layer_type = Column(String(100), nullable=False)  # 'aircraft', 'geojson', 'pmtiles', etc.
    data_source_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="SET NULL"))
    style_config = Column(JSONB)  # Styling configuration
    is_visible = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    z_index = Column(Integer, default=0)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="map_layers")
    data_source = relationship("DataSource", back_populates="map_layers")
    
    def __repr__(self) -> str:
        return f"<MapLayer(id={self.id}, name='{self.name}', type='{self.layer_type}')>"
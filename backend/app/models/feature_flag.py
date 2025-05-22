"""
Feature flag model for feature toggles
"""
from sqlalchemy import Boolean, Column, ForeignKey, String, Text, UniqueConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base


class FeatureFlag(Base):
    """Feature flag model for toggling features per tenant"""
    
    __tablename__ = "feature_flags"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    enabled = Column(Boolean, default=False, nullable=False)
    description = Column(Text)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="feature_flags")
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_tenant_feature"),
    )
    
    def __repr__(self) -> str:
        return f"<FeatureFlag(id={self.id}, name='{self.name}', enabled={self.enabled})>"
"""
Synergy model database model.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, DECIMAL, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SynergyModel(Base):
    """Model for synergy assumptions and realization schedules."""
    
    __tablename__ = "synergy_models"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    assumptions_id = Column(Integer, ForeignKey("assumptions.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False)  # operational_overhead, procurement_efficiency, workforce_consolidation, shared_infrastructure
    description = Column(Text)
    target_value = Column(DECIMAL(15, 2), nullable=False)  # Annual synergy value at full realization
    realization_schedule = Column(JSON, nullable=False)  # Array of {year: int, percentage: float}
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    assumptions = relationship("Assumptions", back_populates="synergy_models")
    
    def __repr__(self):
        return f"<SynergyModel(category={self.category}, target_value={self.target_value})>"

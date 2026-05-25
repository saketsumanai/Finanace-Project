"""
Scenario database model.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, UniqueConstraint, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Scenario(Base):
    """Model for valuation scenarios (Bull/Base/Bear/Custom)."""
    
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    assumptions_id = Column(Integer, ForeignKey("assumptions.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    scenario_type = Column(String(50), nullable=False)  # bull, base, bear, custom
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", backref="scenarios")
    assumptions = relationship("Assumptions", back_populates="scenarios")
    valuation_outputs = relationship("ValuationOutput", back_populates="scenario", cascade="all, delete-orphan")
    
    # Unique constraint on project_id and name
    __table_args__ = (
        UniqueConstraint('project_id', 'name', name='uq_scenario_project_name'),
    )
    
    def __repr__(self):
        return f"<Scenario(name={self.name}, type={self.scenario_type})>"

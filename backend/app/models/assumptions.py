"""
Assumptions database model for financial modeling.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, DECIMAL, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Assumptions(Base):
    """Model for financial modeling assumptions."""
    
    __tablename__ = "assumptions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(Integer, nullable=False, default=1)
    name = Column(String(255), nullable=False)
    
    # Production assumptions
    decline_curve_type = Column(String(50), nullable=False)  # exponential, hyperbolic, harmonic
    decline_rate = Column(DECIMAL(5, 4))  # e.g., 0.1500 for 15%
    hyperbolic_b = Column(DECIMAL(3, 2))  # e.g., 0.50 for b=0.5
    oil_price_forecast = Column(JSON)  # Array of {year: int, price: float}
    gas_price_forecast = Column(JSON)  # Array of {year: int, price: float}
    
    # Cost assumptions
    opex_inflation_rate = Column(DECIMAL(5, 4))  # e.g., 0.0300 for 3%
    capex_schedule = Column(JSON)  # Array of {year: int, amount: float}
    transportation_cost_per_unit = Column(DECIMAL(10, 2))
    ga_annual = Column(DECIMAL(15, 2))  # Annual G&A expense
    
    # Deal assumptions
    purchase_price = Column(DECIMAL(15, 2))
    debt_amount = Column(DECIMAL(15, 2))
    equity_amount = Column(DECIMAL(15, 2))
    discount_rate = Column(DECIMAL(5, 4))  # WACC
    tax_rate = Column(DECIMAL(5, 4))  # e.g., 0.2100 for 21%
    exit_multiple = Column(DECIMAL(4, 2))  # e.g., 5.50 for 5.5x EBITDA
    forecast_years = Column(Integer, default=20)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", backref="assumptions")
    synergy_models = relationship("SynergyModel", back_populates="assumptions", cascade="all, delete-orphan")
    scenarios = relationship("Scenario", back_populates="assumptions", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Assumptions(project_id={self.project_id}, version={self.version}, name={self.name})>"

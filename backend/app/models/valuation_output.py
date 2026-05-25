"""
Valuation output database model.
"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ValuationOutput(Base):
    """Model for storing valuation calculation results."""
    
    __tablename__ = "valuation_outputs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id", ondelete="CASCADE"), nullable=False, index=True)
    year = Column(Integer, nullable=False)  # 0 = initial year, 1-N = forecast years
    
    # Production forecasts
    oil_production = Column(DECIMAL(15, 2))  # barrels
    gas_production = Column(DECIMAL(15, 2))  # MCF
    
    # Financial forecasts
    revenue = Column(DECIMAL(15, 2))
    opex = Column(DECIMAL(15, 2))
    capex = Column(DECIMAL(15, 2))
    ebitda = Column(DECIMAL(15, 2))
    ebitdax = Column(DECIMAL(15, 2))
    depreciation = Column(DECIMAL(15, 2))
    interest_expense = Column(DECIMAL(15, 2))
    taxes = Column(DECIMAL(15, 2))
    free_cash_flow = Column(DECIMAL(15, 2))
    
    # Synergies
    synergy_value = Column(DECIMAL(15, 2))
    
    # Debt
    debt_balance = Column(DECIMAL(15, 2))
    debt_service = Column(DECIMAL(15, 2))
    
    # Valuation metrics (stored in year 0 or summary record)
    npv = Column(DECIMAL(15, 2))
    irr = Column(DECIMAL(7, 4))  # e.g., 0.1845 for 18.45%
    payback_period = Column(DECIMAL(5, 2))  # years
    roic = Column(DECIMAL(7, 4))
    terminal_value = Column(DECIMAL(15, 2))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    scenario = relationship("Scenario", back_populates="valuation_outputs")
    
    # Unique constraint on scenario_id and year
    __table_args__ = (
        UniqueConstraint('scenario_id', 'year', name='uq_valuation_scenario_year'),
    )
    
    def __repr__(self):
        return f"<ValuationOutput(scenario_id={self.scenario_id}, year={self.year})>"

"""
Pydantic schemas for scenarios and valuation outputs.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class ScenarioCreate(BaseModel):
    """Schema for creating a scenario."""
    project_id: int
    assumptions_id: int
    name: str = Field(..., min_length=1, max_length=255)
    scenario_type: str = Field(..., description="Scenario type")
    description: Optional[str] = Field(None, description="Scenario description")
    
    @validator('scenario_type')
    def validate_scenario_type(cls, v):
        valid_types = ['bull', 'base', 'bear', 'custom']
        if v not in valid_types:
            raise ValueError(f"Scenario type must be one of: {', '.join(valid_types)}")
        return v


class ScenarioUpdate(BaseModel):
    """Schema for updating a scenario."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    assumptions_id: Optional[int] = None
    description: Optional[str] = None


class ScenarioResponse(BaseModel):
    """Schema for scenario response."""
    id: int
    project_id: int
    assumptions_id: int
    name: str
    scenario_type: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ValuationMetrics(BaseModel):
    """Valuation metrics summary."""
    npv: Optional[float] = Field(None, description="Net Present Value")
    irr: Optional[float] = Field(None, description="Internal Rate of Return")
    payback_period: Optional[float] = Field(None, description="Payback period in years")
    roi: Optional[float] = Field(None, description="Return on Investment")
    roic: Optional[float] = Field(None, description="Return on Invested Capital")
    profitability_index: Optional[float] = Field(None, description="Profitability Index")
    terminal_value: Optional[float] = Field(None, description="Terminal Value")


class AnnualData(BaseModel):
    """Annual valuation data."""
    year: int
    oil_production: float
    gas_production: float
    revenue: float
    opex: float
    capex: float
    ebitda: float
    synergy_value: float
    free_cash_flow: float
    taxes: float


class ValuationSummary(BaseModel):
    """Summary of valuation results."""
    scenario_id: str
    scenario_name: str
    scenario_type: str
    metrics: ValuationMetrics
    summary_financials: Optional[Dict[str, float]] = None
    production_summary: Optional[Dict[str, Any]] = None


class ValuationResults(BaseModel):
    """Complete valuation results."""
    scenario_id: str
    scenario_name: str
    scenario_type: str
    metrics: ValuationMetrics
    annual_data: List[AnnualData]


class RunValuationRequest(BaseModel):
    """Request to run valuation."""
    scenario_id: int
    periods_per_year: int = Field(default=12, ge=1, le=12, description="Periods per year (1=annual, 12=monthly)")


class ScenarioComparison(BaseModel):
    """Comparison of multiple scenarios."""
    scenario_id: str
    scenario_name: str
    scenario_type: str
    npv: Optional[float]
    irr: Optional[float]
    payback_period: Optional[float]
    roic: Optional[float]


class ComparisonResults(BaseModel):
    """Results of scenario comparison."""
    scenarios: List[ScenarioComparison]

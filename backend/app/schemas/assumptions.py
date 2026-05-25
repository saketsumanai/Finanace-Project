"""
Pydantic schemas for assumptions and synergy models.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class PriceForecast(BaseModel):
    """Price forecast for a specific year."""
    year: int = Field(..., ge=1, le=50, description="Forecast year")
    price: float = Field(..., gt=0, description="Price in USD")


class CapexScheduleItem(BaseModel):
    """CAPEX schedule item for a specific year."""
    year: int = Field(..., ge=1, le=50, description="Year")
    amount: float = Field(..., ge=0, description="CAPEX amount in USD")


class SynergyRealizationItem(BaseModel):
    """Synergy realization schedule item."""
    year: int = Field(..., ge=1, le=20, description="Year")
    percentage: float = Field(..., ge=0, le=1, description="Realization percentage (0-1)")


class SynergyModelCreate(BaseModel):
    """Schema for creating a synergy model."""
    category: str = Field(..., description="Synergy category")
    description: Optional[str] = Field(None, description="Description of synergy")
    target_value: float = Field(..., gt=0, description="Annual synergy value at full realization")
    realization_schedule: List[SynergyRealizationItem] = Field(..., description="Realization schedule")
    
    @validator('category')
    def validate_category(cls, v):
        valid_categories = [
            'operational_overhead',
            'procurement_efficiency',
            'workforce_consolidation',
            'shared_infrastructure'
        ]
        if v not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return v


class SynergyModelResponse(BaseModel):
    """Schema for synergy model response."""
    id: int
    assumptions_id: int
    category: str
    description: Optional[str]
    target_value: float
    realization_schedule: List[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AssumptionsCreate(BaseModel):
    """Schema for creating assumptions."""
    project_id: int
    name: str = Field(..., min_length=1, max_length=255)
    version: int = Field(default=1, ge=1)
    
    # Production assumptions
    decline_curve_type: str = Field(..., description="Decline curve type")
    decline_rate: float = Field(..., ge=0, le=1, description="Decline rate (0-1)")
    hyperbolic_b: Optional[float] = Field(None, ge=0, lt=1, description="Hyperbolic b factor (0-1)")
    oil_price_forecast: List[PriceForecast] = Field(default=[], description="Oil price forecast")
    gas_price_forecast: List[PriceForecast] = Field(default=[], description="Gas price forecast")
    
    # Cost assumptions
    opex_inflation_rate: float = Field(default=0.03, ge=-0.1, le=0.5, description="OPEX inflation rate")
    capex_schedule: List[CapexScheduleItem] = Field(default=[], description="CAPEX schedule")
    transportation_cost_per_unit: float = Field(default=0, ge=0, description="Transportation cost per BOE")
    ga_annual: float = Field(default=0, ge=0, description="Annual G&A expense")
    
    # Deal assumptions
    purchase_price: float = Field(..., gt=0, description="Purchase price")
    debt_amount: float = Field(default=0, ge=0, description="Debt amount")
    equity_amount: float = Field(default=0, ge=0, description="Equity amount")
    discount_rate: float = Field(default=0.12, gt=0, le=1, description="Discount rate (WACC)")
    tax_rate: float = Field(default=0.21, ge=0, le=1, description="Tax rate")
    exit_multiple: float = Field(default=5.0, gt=0, le=20, description="Exit EBITDA multiple")
    forecast_years: int = Field(default=20, ge=1, le=50, description="Forecast period in years")
    
    @validator('decline_curve_type')
    def validate_decline_curve_type(cls, v):
        valid_types = ['exponential', 'hyperbolic', 'harmonic']
        if v not in valid_types:
            raise ValueError(f"Decline curve type must be one of: {', '.join(valid_types)}")
        return v
    
    @validator('hyperbolic_b')
    def validate_hyperbolic_b(cls, v, values):
        if values.get('decline_curve_type') == 'hyperbolic' and v is None:
            raise ValueError("hyperbolic_b is required when decline_curve_type is 'hyperbolic'")
        return v


class AssumptionsUpdate(BaseModel):
    """Schema for updating assumptions."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    
    # Production assumptions
    decline_curve_type: Optional[str] = None
    decline_rate: Optional[float] = Field(None, ge=0, le=1)
    hyperbolic_b: Optional[float] = Field(None, ge=0, lt=1)
    oil_price_forecast: Optional[List[PriceForecast]] = None
    gas_price_forecast: Optional[List[PriceForecast]] = None
    
    # Cost assumptions
    opex_inflation_rate: Optional[float] = Field(None, ge=-0.1, le=0.5)
    capex_schedule: Optional[List[CapexScheduleItem]] = None
    transportation_cost_per_unit: Optional[float] = Field(None, ge=0)
    ga_annual: Optional[float] = Field(None, ge=0)
    
    # Deal assumptions
    purchase_price: Optional[float] = Field(None, gt=0)
    debt_amount: Optional[float] = Field(None, ge=0)
    equity_amount: Optional[float] = Field(None, ge=0)
    discount_rate: Optional[float] = Field(None, gt=0, le=1)
    tax_rate: Optional[float] = Field(None, ge=0, le=1)
    exit_multiple: Optional[float] = Field(None, gt=0, le=20)
    forecast_years: Optional[int] = Field(None, ge=1, le=50)


class AssumptionsResponse(BaseModel):
    """Schema for assumptions response."""
    id: int
    project_id: int
    version: int
    name: str
    
    # Production assumptions
    decline_curve_type: str
    decline_rate: float
    hyperbolic_b: Optional[float]
    oil_price_forecast: Optional[List[dict]]
    gas_price_forecast: Optional[List[dict]]
    
    # Cost assumptions
    opex_inflation_rate: Optional[float]
    capex_schedule: Optional[List[dict]]
    transportation_cost_per_unit: Optional[float]
    ga_annual: Optional[float]
    
    # Deal assumptions
    purchase_price: Optional[float]
    debt_amount: Optional[float]
    equity_amount: Optional[float]
    discount_rate: Optional[float]
    tax_rate: Optional[float]
    exit_multiple: Optional[float]
    forecast_years: Optional[int]
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AssumptionsWithSynergies(AssumptionsResponse):
    """Schema for assumptions with synergy models."""
    synergy_models: List[SynergyModelResponse] = []
    
    class Config:
        from_attributes = True

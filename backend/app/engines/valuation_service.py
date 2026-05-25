"""
Valuation service - Main orchestrator for financial modeling and valuation.

Coordinates all calculation engines to produce comprehensive valuation outputs:
- Production forecasting (decline curves)
- Revenue modeling
- Cost forecasting
- Synergy calculations
- Cash flow modeling
- IRR/NPV calculations
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from sqlalchemy.orm import Session

from app.engines.decline_curves import create_decline_curve
from app.engines.forecasting_engine import ForecastingEngine
from app.engines.synergy_engine import SynergyEngine
from app.engines.irr_engine import IRREngine
from app.models.production_data import ProductionData
from app.models.financial_data import FinancialData
from app.models.assumptions import Assumptions
from app.models.synergy_model import SynergyModel
from app.models.scenario import Scenario
from app.models.valuation_output import ValuationOutput


class ValuationService:
    """
    Main valuation service that orchestrates all calculation engines.
    
    This service:
    1. Loads historical data
    2. Applies assumptions
    3. Generates production forecasts
    4. Calculates revenue and costs
    5. Models synergies
    6. Computes cash flows
    7. Calculates valuation metrics (NPV, IRR, etc.)
    8. Stores results in database
    """
    
    def __init__(self, db: Session):
        """
        Initialize valuation service.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.forecasting_engine = ForecastingEngine()
        self.synergy_engine = SynergyEngine()
        self.irr_engine = IRREngine()
    
    def run_valuation(
        self,
        scenario_id: str,
        periods_per_year: int = 12
    ) -> Dict:
        """
        Run complete valuation for a scenario.
        
        Args:
            scenario_id: UUID of scenario to value
            periods_per_year: Number of periods per year (12 for monthly, 1 for annual)
        
        Returns:
            Dict with valuation results and summary metrics
        
        Raises:
            ValueError: If scenario not found or missing data
        """
        # Load scenario and assumptions
        scenario = self.db.query(Scenario).filter(Scenario.id == scenario_id).first()
        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        assumptions = scenario.assumptions
        project_id = scenario.project_id
        
        # Load historical data
        historical_production = self._load_historical_production(project_id)
        historical_financial = self._load_historical_financial(project_id)
        
        # Calculate initial rates from historical data
        initial_oil_rate, initial_gas_rate = self._calculate_initial_rates(
            historical_production,
            periods_per_year
        )
        
        # Calculate forecast periods
        forecast_years = assumptions.forecast_years or 20
        periods = forecast_years * periods_per_year
        
        # Generate production forecast
        production_df = self.forecasting_engine.forecast_production(
            initial_oil_rate=initial_oil_rate,
            initial_gas_rate=initial_gas_rate,
            decline_curve_type=assumptions.decline_curve_type,
            decline_rate=float(assumptions.decline_rate),
            periods=periods,
            b_factor=float(assumptions.hyperbolic_b) if assumptions.hyperbolic_b else None
        )
        
        # Generate revenue forecast
        revenue_df = self.forecasting_engine.forecast_revenue(
            production_df=production_df,
            oil_price_forecast=assumptions.oil_price_forecast or [],
            gas_price_forecast=assumptions.gas_price_forecast or [],
            periods_per_year=periods_per_year
        )
        
        # Generate cost forecasts
        base_opex = self._calculate_base_opex(historical_financial)
        opex = self.forecasting_engine.forecast_opex(
            base_opex=base_opex,
            inflation_rate=float(assumptions.opex_inflation_rate or 0.03),
            periods=periods,
            periods_per_year=periods_per_year
        )
        
        capex = self.forecasting_engine.forecast_capex(
            capex_schedule=assumptions.capex_schedule or [],
            periods=periods,
            periods_per_year=periods_per_year
        )
        
        # Calculate synergies
        synergy_models = self.db.query(SynergyModel).filter(
            SynergyModel.assumptions_id == assumptions.id
        ).all()
        
        synergy_models_list = [
            {
                'category': sm.category,
                'target_value': float(sm.target_value),
                'realization_schedule': sm.realization_schedule
            }
            for sm in synergy_models
        ]
        
        synergy_values = self.synergy_engine.calculate_synergies(
            synergy_models=synergy_models_list,
            periods=periods,
            periods_per_year=periods_per_year
        )
        
        # Create comprehensive cash flow forecast
        cash_flow_df = self.forecasting_engine.create_cash_flow_forecast(
            production_df=production_df,
            revenue_df=revenue_df,
            opex=opex,
            capex=capex,
            synergy_values=synergy_values,
            ga_expense=float(assumptions.ga_annual or 0),
            transportation_cost_per_boe=float(assumptions.transportation_cost_per_unit or 0),
            tax_rate=float(assumptions.tax_rate or 0.21),
            depreciation_rate=0.15,
            periods_per_year=periods_per_year
        )
        
        # Aggregate to annual for valuation calculations
        annual_df = self.forecasting_engine.aggregate_by_period(
            df=cash_flow_df,
            source_periods_per_year=periods_per_year,
            target_periods_per_year=1
        )
        
        # Calculate terminal value
        terminal_ebitda = annual_df['ebitda'].iloc[-1]
        exit_multiple = float(assumptions.exit_multiple or 5.0)
        terminal_value = terminal_ebitda * exit_multiple
        
        # Build cash flow array for IRR/NPV calculation
        cash_flows = self._build_cash_flow_array(
            annual_df=annual_df,
            purchase_price=float(assumptions.purchase_price or 0),
            terminal_value=terminal_value
        )
        
        # Calculate valuation metrics
        discount_rate = float(assumptions.discount_rate or 0.12)
        
        irr = self.irr_engine.calculate_irr(cash_flows)
        npv = self.irr_engine.calculate_npv(cash_flows, discount_rate)
        payback_period = self.irr_engine.calculate_payback_period(cash_flows)
        roi = self.irr_engine.calculate_roi(cash_flows)
        profitability_index = self.irr_engine.calculate_profitability_index(cash_flows, discount_rate)
        
        # Calculate ROIC
        invested_capital = float(assumptions.purchase_price or 0)
        avg_nopat = annual_df['ebitda'].mean() * (1 - float(assumptions.tax_rate or 0.21))
        roic = avg_nopat / invested_capital if invested_capital > 0 else None
        
        # Store results in database
        self._store_valuation_outputs(
            scenario_id=scenario_id,
            annual_df=annual_df,
            npv=npv,
            irr=irr,
            payback_period=payback_period,
            roic=roic,
            terminal_value=terminal_value
        )
        
        # Prepare summary
        summary = {
            'scenario_id': str(scenario_id),
            'scenario_name': scenario.name,
            'scenario_type': scenario.scenario_type,
            'metrics': {
                'npv': float(npv) if npv else None,
                'irr': float(irr) if irr else None,
                'payback_period': float(payback_period) if payback_period else None,
                'roi': float(roi) if roi else None,
                'roic': float(roic) if roic else None,
                'profitability_index': float(profitability_index) if profitability_index else None,
                'terminal_value': float(terminal_value)
            },
            'summary_financials': {
                'total_revenue': float(annual_df['total_revenue'].sum()),
                'total_opex': float(annual_df['opex'].sum()),
                'total_capex': float(annual_df['capex'].sum()),
                'total_synergies': float(annual_df['synergy_value'].sum()),
                'total_ebitda': float(annual_df['ebitda'].sum()),
                'total_fcf': float(annual_df['free_cash_flow'].sum()),
                'avg_annual_ebitda': float(annual_df['ebitda'].mean()),
                'year_1_ebitda': float(annual_df['ebitda'].iloc[0]) if len(annual_df) > 0 else 0,
                'final_year_ebitda': float(annual_df['ebitda'].iloc[-1]) if len(annual_df) > 0 else 0
            },
            'production_summary': {
                'initial_oil_rate': float(initial_oil_rate),
                'initial_gas_rate': float(initial_gas_rate),
                'total_oil_production': float(annual_df['oil_production'].sum()),
                'total_gas_production': float(annual_df['gas_production'].sum()),
                'decline_curve_type': assumptions.decline_curve_type,
                'decline_rate': float(assumptions.decline_rate)
            }
        }
        
        return summary
    
    def _load_historical_production(self, project_id: str) -> List[ProductionData]:
        """Load historical production data for a project."""
        return self.db.query(ProductionData).filter(
            ProductionData.project_id == project_id
        ).order_by(ProductionData.date).all()
    
    def _load_historical_financial(self, project_id: str) -> List[FinancialData]:
        """Load historical financial data for a project."""
        return self.db.query(FinancialData).filter(
            FinancialData.project_id == project_id
        ).order_by(FinancialData.date).all()
    
    def _calculate_initial_rates(
        self,
        historical_production: List[ProductionData],
        periods_per_year: int
    ) -> Tuple[float, float]:
        """
        Calculate initial production rates from historical data.
        
        Uses the average of the last 3 months as the initial rate.
        If no historical data, uses default values.
        """
        if not historical_production:
            # Use default initial rates if no historical data
            return 1000.0, 5000.0  # Default: 1000 bbl/day oil, 5000 MCF/day gas
        
        # Get last 3 data points
        recent_data = historical_production[-3:]
        
        oil_rates = [float(p.oil_volume or 0) for p in recent_data]
        gas_rates = [float(p.gas_volume or 0) for p in recent_data]
        
        initial_oil_rate = sum(oil_rates) / len(oil_rates)
        initial_gas_rate = sum(gas_rates) / len(gas_rates)
        
        return initial_oil_rate, initial_gas_rate
    
    def _calculate_base_opex(self, historical_financial: List[FinancialData]) -> float:
        """
        Calculate base annual OPEX from historical data.
        
        Uses the average of the last 12 months.
        If no historical data, uses default value.
        """
        if not historical_financial:
            return 1000000.0  # Default: $1M annual OPEX
        
        # Get last 12 data points
        recent_data = historical_financial[-12:]
        
        opex_values = [float(f.opex or 0) for f in recent_data]
        
        # Sum to get annual OPEX
        annual_opex = sum(opex_values)
        
        return annual_opex
    
    def _build_cash_flow_array(
        self,
        annual_df: pd.DataFrame,
        purchase_price: float,
        terminal_value: float
    ) -> List[float]:
        """
        Build cash flow array for IRR/NPV calculation.
        
        Format: [Year 0: -Purchase Price, Year 1-N: FCF, Year N: FCF + Terminal Value]
        """
        cash_flows = [-purchase_price]  # Year 0: Initial investment
        
        # Years 1 to N-1: Free cash flows
        for i in range(len(annual_df) - 1):
            cash_flows.append(float(annual_df['free_cash_flow'].iloc[i]))
        
        # Year N: FCF + Terminal Value
        if len(annual_df) > 0:
            final_fcf = float(annual_df['free_cash_flow'].iloc[-1])
            cash_flows.append(final_fcf + terminal_value)
        
        return cash_flows
    
    def _store_valuation_outputs(
        self,
        scenario_id: str,
        annual_df: pd.DataFrame,
        npv: Optional[float],
        irr: Optional[float],
        payback_period: Optional[float],
        roic: Optional[float],
        terminal_value: float
    ):
        """
        Store valuation outputs in database.
        
        Deletes existing outputs for the scenario and creates new ones.
        """
        # Delete existing outputs
        self.db.query(ValuationOutput).filter(
            ValuationOutput.scenario_id == scenario_id
        ).delete()
        
        # Create new outputs for each year
        for idx, row in annual_df.iterrows():
            year = int(row['period']) + 1  # Convert 0-based to 1-based
            
            output = ValuationOutput(
                scenario_id=scenario_id,
                year=year,
                oil_production=Decimal(str(row['oil_production'])),
                gas_production=Decimal(str(row['gas_production'])),
                revenue=Decimal(str(row['total_revenue'])),
                opex=Decimal(str(row['opex'])),
                capex=Decimal(str(row['capex'])),
                ebitda=Decimal(str(row['ebitda'])),
                ebitdax=Decimal(str(row['ebitda'])),  # EBITDAX = EBITDA for now
                depreciation=Decimal(str(row['depreciation'])),
                interest_expense=Decimal('0'),  # Not modeled yet
                taxes=Decimal(str(row['taxes'])),
                free_cash_flow=Decimal(str(row['free_cash_flow'])),
                synergy_value=Decimal(str(row['synergy_value'])),
                debt_balance=Decimal('0'),  # Not modeled yet
                debt_service=Decimal('0')  # Not modeled yet
            )
            
            # Store metrics in year 1 record
            if year == 1:
                output.npv = Decimal(str(npv)) if npv is not None else None
                output.irr = Decimal(str(irr)) if irr is not None else None
                output.payback_period = Decimal(str(payback_period)) if payback_period is not None else None
                output.roic = Decimal(str(roic)) if roic is not None else None
                output.terminal_value = Decimal(str(terminal_value))
            
            self.db.add(output)
        
        self.db.commit()
    
    def get_valuation_results(self, scenario_id: str) -> Dict:
        """
        Retrieve stored valuation results for a scenario.
        
        Args:
            scenario_id: UUID of scenario
        
        Returns:
            Dict with valuation results
        """
        scenario = self.db.query(Scenario).filter(Scenario.id == scenario_id).first()
        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        outputs = self.db.query(ValuationOutput).filter(
            ValuationOutput.scenario_id == scenario_id
        ).order_by(ValuationOutput.year).all()
        
        if not outputs:
            return {
                'scenario_id': str(scenario_id),
                'scenario_name': scenario.name,
                'error': 'No valuation results found. Run valuation first.'
            }
        
        # Extract metrics from year 1 record
        first_output = outputs[0]
        
        # Build annual data
        annual_data = []
        for output in outputs:
            annual_data.append({
                'year': output.year,
                'oil_production': float(output.oil_production or 0),
                'gas_production': float(output.gas_production or 0),
                'revenue': float(output.revenue or 0),
                'opex': float(output.opex or 0),
                'capex': float(output.capex or 0),
                'ebitda': float(output.ebitda or 0),
                'synergy_value': float(output.synergy_value or 0),
                'free_cash_flow': float(output.free_cash_flow or 0),
                'taxes': float(output.taxes or 0)
            })
        
        return {
            'scenario_id': str(scenario_id),
            'scenario_name': scenario.name,
            'scenario_type': scenario.scenario_type,
            'metrics': {
                'npv': float(first_output.npv) if first_output.npv else None,
                'irr': float(first_output.irr) if first_output.irr else None,
                'payback_period': float(first_output.payback_period) if first_output.payback_period else None,
                'roic': float(first_output.roic) if first_output.roic else None,
                'terminal_value': float(first_output.terminal_value) if first_output.terminal_value else None
            },
            'annual_data': annual_data
        }
    
    def compare_scenarios(self, scenario_ids: List[str]) -> Dict:
        """
        Compare multiple scenarios side-by-side.
        
        Args:
            scenario_ids: List of scenario UUIDs to compare
        
        Returns:
            Dict with comparison data
        """
        scenarios_data = []
        
        for scenario_id in scenario_ids:
            try:
                result = self.get_valuation_results(scenario_id)
                scenarios_data.append(result)
            except ValueError:
                continue
        
        if not scenarios_data:
            return {'error': 'No valid scenarios found'}
        
        # Build comparison summary
        comparison = {
            'scenarios': []
        }
        
        for data in scenarios_data:
            comparison['scenarios'].append({
                'scenario_id': data['scenario_id'],
                'scenario_name': data['scenario_name'],
                'scenario_type': data['scenario_type'],
                'npv': data['metrics'].get('npv'),
                'irr': data['metrics'].get('irr'),
                'payback_period': data['metrics'].get('payback_period'),
                'roic': data['metrics'].get('roic')
            })
        
        return comparison

"""
Forecasting engine for production, revenue, and cost projections.

Generates multi-year forecasts for:
- Oil and gas production (using decline curves)
- Revenue (production * prices)
- Operating expenses (OPEX)
- Capital expenditures (CAPEX)
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from decimal import Decimal

from app.engines.decline_curves import create_decline_curve


class ForecastingEngine:
    """Engine for forecasting production, revenue, and costs."""
    
    def __init__(self):
        """Initialize forecasting engine."""
        pass
    
    def forecast_production(
        self,
        initial_oil_rate: float,
        initial_gas_rate: float,
        decline_curve_type: str,
        decline_rate: float,
        periods: int,
        b_factor: Optional[float] = None
    ) -> pd.DataFrame:
        """
        Forecast oil and gas production using decline curves.
        
        Args:
            initial_oil_rate: Initial oil production rate (barrels/month)
            initial_gas_rate: Initial gas production rate (MCF/month)
            decline_curve_type: Type of decline curve (exponential, hyperbolic, harmonic)
            decline_rate: Decline rate (decimal)
            periods: Number of periods to forecast
            b_factor: Hyperbolic exponent (required for hyperbolic)
        
        Returns:
            DataFrame with columns: period, oil_production, gas_production
        
        Example:
            >>> engine = ForecastingEngine()
            >>> df = engine.forecast_production(
            ...     initial_oil_rate=1000,
            ...     initial_gas_rate=5000,
            ...     decline_curve_type='hyperbolic',
            ...     decline_rate=0.15,
            ...     periods=240,  # 20 years * 12 months
            ...     b_factor=0.5
            ... )
        """
        # Create decline curves for oil and gas
        oil_curve = create_decline_curve(
            curve_type=decline_curve_type,
            initial_rate=initial_oil_rate,
            decline_rate=decline_rate,
            b_factor=b_factor
        )
        
        gas_curve = create_decline_curve(
            curve_type=decline_curve_type,
            initial_rate=initial_gas_rate,
            decline_rate=decline_rate,
            b_factor=b_factor
        )
        
        # Generate forecasts
        oil_production = oil_curve.forecast(periods)
        gas_production = gas_curve.forecast(periods)
        
        # Create DataFrame
        df = pd.DataFrame({
            'period': np.arange(periods),
            'oil_production': oil_production,
            'gas_production': gas_production
        })
        
        return df
    
    def forecast_revenue(
        self,
        production_df: pd.DataFrame,
        oil_price_forecast: List[Dict],
        gas_price_forecast: List[Dict],
        periods_per_year: int = 12
    ) -> pd.DataFrame:
        """
        Forecast revenue based on production and price forecasts.
        
        Args:
            production_df: DataFrame with oil_production and gas_production columns
            oil_price_forecast: List of {year: int, price: float} dicts
            gas_price_forecast: List of {year: int, price: float} dicts
            periods_per_year: Number of periods per year (12 for monthly)
        
        Returns:
            DataFrame with additional columns: oil_price, gas_price, oil_revenue, gas_revenue, total_revenue
        
        Example:
            >>> oil_prices = [
            ...     {'year': 1, 'price': 70.0},
            ...     {'year': 2, 'price': 72.0},
            ...     {'year': 3, 'price': 75.0}
            ... ]
            >>> gas_prices = [
            ...     {'year': 1, 'price': 3.5},
            ...     {'year': 2, 'price': 3.6},
            ...     {'year': 3, 'price': 3.7}
            ... ]
            >>> revenue_df = engine.forecast_revenue(production_df, oil_prices, gas_prices)
        """
        df = production_df.copy()
        
        # Convert price forecasts to arrays
        oil_prices = self._interpolate_prices(oil_price_forecast, len(df), periods_per_year)
        gas_prices = self._interpolate_prices(gas_price_forecast, len(df), periods_per_year)
        
        df['oil_price'] = oil_prices
        df['gas_price'] = gas_prices
        
        # Calculate revenue
        df['oil_revenue'] = df['oil_production'] * df['oil_price']
        df['gas_revenue'] = df['gas_production'] * df['gas_price']
        df['total_revenue'] = df['oil_revenue'] + df['gas_revenue']
        
        return df
    
    def forecast_opex(
        self,
        base_opex: float,
        inflation_rate: float,
        periods: int,
        periods_per_year: int = 12
    ) -> np.ndarray:
        """
        Forecast operating expenses with inflation.
        
        Formula: OPEX(t) = Base_OPEX * (1 + inflation_rate)^(t / periods_per_year)
        
        Args:
            base_opex: Base annual OPEX
            inflation_rate: Annual inflation rate (decimal)
            periods: Number of periods to forecast
            periods_per_year: Number of periods per year
        
        Returns:
            Array of OPEX values (monthly if periods_per_year=12)
        
        Example:
            >>> opex = engine.forecast_opex(
            ...     base_opex=1200000,  # $1.2M annual
            ...     inflation_rate=0.03,  # 3%
            ...     periods=240,  # 20 years * 12 months
            ...     periods_per_year=12
            ... )
        """
        # Convert annual OPEX to per-period OPEX
        base_opex_per_period = base_opex / periods_per_year
        
        # Calculate time in years for each period
        time_in_years = np.arange(periods) / periods_per_year
        
        # Apply inflation
        opex = base_opex_per_period * np.power(1 + inflation_rate, time_in_years)
        
        return opex
    
    def forecast_capex(
        self,
        capex_schedule: List[Dict],
        periods: int,
        periods_per_year: int = 12
    ) -> np.ndarray:
        """
        Forecast capital expenditures based on schedule.
        
        Args:
            capex_schedule: List of {year: int, amount: float} dicts
            periods: Number of periods to forecast
            periods_per_year: Number of periods per year
        
        Returns:
            Array of CAPEX values
        
        Example:
            >>> capex_schedule = [
            ...     {'year': 1, 'amount': 5000000},
            ...     {'year': 2, 'amount': 3000000},
            ...     {'year': 5, 'amount': 2000000}
            ... ]
            >>> capex = engine.forecast_capex(capex_schedule, 240, 12)
        """
        capex = np.zeros(periods)
        
        for item in capex_schedule:
            year = item['year']
            amount = item['amount']
            
            # Distribute CAPEX evenly across the year
            start_period = (year - 1) * periods_per_year
            end_period = min(year * periods_per_year, periods)
            
            if start_period < periods:
                periods_in_year = end_period - start_period
                capex_per_period = amount / periods_in_year
                capex[start_period:end_period] = capex_per_period
        
        return capex
    
    def aggregate_by_period(
        self,
        df: pd.DataFrame,
        source_periods_per_year: int,
        target_periods_per_year: int
    ) -> pd.DataFrame:
        """
        Aggregate data from one time period to another (e.g., monthly to annual).
        
        Args:
            df: DataFrame with period-based data
            source_periods_per_year: Source frequency (e.g., 12 for monthly)
            target_periods_per_year: Target frequency (e.g., 1 for annual)
        
        Returns:
            Aggregated DataFrame
        
        Example:
            >>> # Convert monthly to annual
            >>> annual_df = engine.aggregate_by_period(monthly_df, 12, 1)
        """
        if source_periods_per_year == target_periods_per_year:
            return df.copy()
        
        # Calculate aggregation factor
        agg_factor = source_periods_per_year // target_periods_per_year
        
        # Create year column
        df_copy = df.copy()
        df_copy['year'] = df_copy['period'] // agg_factor
        
        # Define aggregation rules
        agg_rules = {}
        for col in df_copy.columns:
            if col in ['period', 'year']:
                continue
            elif col in ['oil_price', 'gas_price']:
                # Prices: use average
                agg_rules[col] = 'mean'
            else:
                # Production, revenue, costs: sum
                agg_rules[col] = 'sum'
        
        # Aggregate
        result = df_copy.groupby('year').agg(agg_rules).reset_index()
        result.rename(columns={'year': 'period'}, inplace=True)
        
        return result
    
    def _interpolate_prices(
        self,
        price_forecast: List[Dict],
        periods: int,
        periods_per_year: int
    ) -> np.ndarray:
        """
        Interpolate annual price forecasts to period-level prices.
        
        Args:
            price_forecast: List of {year: int, price: float} dicts
            periods: Number of periods
            periods_per_year: Number of periods per year
        
        Returns:
            Array of interpolated prices
        """
        if not price_forecast:
            return np.zeros(periods)
        
        # Sort by year
        price_forecast = sorted(price_forecast, key=lambda x: x['year'])
        
        # Extract years and prices
        years = np.array([item['year'] for item in price_forecast])
        prices = np.array([item['price'] for item in price_forecast])
        
        # Convert periods to years
        period_years = np.arange(periods) / periods_per_year + 1  # Start at year 1
        
        # Interpolate (extrapolate with last value if beyond range)
        interpolated_prices = np.interp(period_years, years, prices)
        
        return interpolated_prices
    
    def create_cash_flow_forecast(
        self,
        production_df: pd.DataFrame,
        revenue_df: pd.DataFrame,
        opex: np.ndarray,
        capex: np.ndarray,
        synergy_values: np.ndarray,
        ga_expense: float,
        transportation_cost_per_boe: float,
        tax_rate: float,
        depreciation_rate: float = 0.15,
        periods_per_year: int = 12
    ) -> pd.DataFrame:
        """
        Create comprehensive cash flow forecast.
        
        Args:
            production_df: Production forecast DataFrame
            revenue_df: Revenue forecast DataFrame
            opex: OPEX array
            capex: CAPEX array
            synergy_values: Synergy values array
            ga_expense: Annual G&A expense
            transportation_cost_per_boe: Transportation cost per barrel of oil equivalent
            tax_rate: Tax rate (decimal)
            depreciation_rate: Annual depreciation rate (decimal)
            periods_per_year: Number of periods per year
        
        Returns:
            DataFrame with complete cash flow forecast
        """
        df = revenue_df.copy()
        
        # Add costs
        df['opex'] = opex
        df['capex'] = capex
        df['synergy_value'] = synergy_values
        
        # Calculate transportation costs (based on total BOE)
        # Conversion: 6 MCF gas = 1 BOE
        df['boe'] = df['oil_production'] + (df['gas_production'] / 6.0)
        df['transportation_cost'] = df['boe'] * transportation_cost_per_boe
        
        # G&A (distributed per period)
        df['ga_expense'] = ga_expense / periods_per_year
        
        # Calculate EBITDA
        df['ebitda'] = (
            df['total_revenue']
            - df['opex']
            - df['transportation_cost']
            - df['ga_expense']
            + df['synergy_value']
        )
        
        # Calculate depreciation (on cumulative CAPEX)
        cumulative_capex = np.cumsum(capex)
        df['depreciation'] = cumulative_capex * (depreciation_rate / periods_per_year)
        
        # Calculate taxable income
        df['taxable_income'] = df['ebitda'] - df['depreciation']
        
        # Calculate taxes (only on positive income)
        df['taxes'] = np.where(df['taxable_income'] > 0, df['taxable_income'] * tax_rate, 0)
        
        # Calculate free cash flow
        df['free_cash_flow'] = df['ebitda'] - df['capex'] - df['taxes']
        
        return df

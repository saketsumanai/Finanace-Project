"""
Synergy calculation engine for M&A value creation modeling.

Implements synergy categories:
- Operational overhead reduction
- Procurement efficiencies
- Workforce consolidation
- Shared infrastructure

Applies realization schedules to model gradual synergy capture.
"""
import numpy as np
from typing import List, Dict


class SynergyEngine:
    """Engine for calculating M&A synergies with realization schedules."""
    
    def __init__(self):
        """Initialize synergy engine."""
        pass
    
    def calculate_synergies(
        self,
        synergy_models: List[Dict],
        periods: int,
        periods_per_year: int = 12
    ) -> np.ndarray:
        """
        Calculate total synergy values over time with realization schedules.
        
        Args:
            synergy_models: List of synergy model dicts with:
                - category: str (operational_overhead, procurement_efficiency, etc.)
                - target_value: float (annual synergy at full realization)
                - realization_schedule: List[Dict] with {year: int, percentage: float}
            periods: Number of periods to forecast
            periods_per_year: Number of periods per year (12 for monthly)
        
        Returns:
            Array of total synergy values per period
        
        Example:
            >>> engine = SynergyEngine()
            >>> synergy_models = [
            ...     {
            ...         'category': 'operational_overhead',
            ...         'target_value': 2000000,  # $2M annual savings
            ...         'realization_schedule': [
            ...             {'year': 1, 'percentage': 0.25},
            ...             {'year': 2, 'percentage': 0.60},
            ...             {'year': 3, 'percentage': 0.85},
            ...             {'year': 4, 'percentage': 1.00}
            ...         ]
            ...     },
            ...     {
            ...         'category': 'procurement_efficiency',
            ...         'target_value': 1500000,  # $1.5M annual savings
            ...         'realization_schedule': [
            ...             {'year': 1, 'percentage': 0.30},
            ...             {'year': 2, 'percentage': 0.70},
            ...             {'year': 3, 'percentage': 1.00}
            ...         ]
            ...     }
            ... ]
            >>> synergies = engine.calculate_synergies(synergy_models, 240, 12)
        """
        total_synergies = np.zeros(periods)
        
        for model in synergy_models:
            target_value = model['target_value']
            realization_schedule = model['realization_schedule']
            
            # Calculate synergy for this model
            model_synergies = self.apply_realization_schedule(
                target_value=target_value,
                realization_schedule=realization_schedule,
                periods=periods,
                periods_per_year=periods_per_year
            )
            
            # Add to total
            total_synergies += model_synergies
        
        return total_synergies
    
    def apply_realization_schedule(
        self,
        target_value: float,
        realization_schedule: List[Dict],
        periods: int,
        periods_per_year: int = 12
    ) -> np.ndarray:
        """
        Apply realization schedule to target synergy value.
        
        The realization schedule defines what percentage of the target synergy
        is achieved in each year. Values are interpolated between years.
        
        Args:
            target_value: Annual synergy value at 100% realization
            realization_schedule: List of {year: int, percentage: float} dicts
            periods: Number of periods to forecast
            periods_per_year: Number of periods per year
        
        Returns:
            Array of realized synergy values per period
        
        Example:
            >>> schedule = [
            ...     {'year': 1, 'percentage': 0.25},  # 25% in year 1
            ...     {'year': 2, 'percentage': 0.60},  # 60% in year 2
            ...     {'year': 3, 'percentage': 0.85},  # 85% in year 3
            ...     {'year': 4, 'percentage': 1.00}   # 100% in year 4+
            ... ]
            >>> synergies = engine.apply_realization_schedule(2000000, schedule, 240, 12)
        """
        if not realization_schedule:
            # No schedule provided, assume immediate full realization
            return np.full(periods, target_value / periods_per_year)
        
        # Sort schedule by year
        schedule = sorted(realization_schedule, key=lambda x: x['year'])
        
        # Extract years and percentages
        years = np.array([item['year'] for item in schedule])
        percentages = np.array([item['percentage'] for item in schedule])
        
        # Add year 0 with 0% realization
        years = np.insert(years, 0, 0)
        percentages = np.insert(percentages, 0, 0.0)
        
        # Convert periods to years
        period_years = np.arange(periods) / periods_per_year
        
        # Interpolate realization percentages
        # Use 'extrapolate' to maintain final percentage beyond last year
        realized_percentages = np.interp(
            period_years,
            years,
            percentages,
            left=0.0,
            right=percentages[-1]  # Maintain final percentage
        )
        
        # Calculate realized synergy values (per period)
        target_value_per_period = target_value / periods_per_year
        realized_synergies = target_value_per_period * realized_percentages
        
        return realized_synergies
    
    def create_standard_realization_schedule(
        self,
        schedule_type: str = 'standard'
    ) -> List[Dict]:
        """
        Create a standard synergy realization schedule.
        
        Args:
            schedule_type: Type of schedule ('aggressive', 'standard', 'conservative')
        
        Returns:
            List of {year: int, percentage: float} dicts
        
        Example:
            >>> engine = SynergyEngine()
            >>> schedule = engine.create_standard_realization_schedule('standard')
            >>> # Returns: [
            >>> #     {'year': 1, 'percentage': 0.25},
            >>> #     {'year': 2, 'percentage': 0.60},
            >>> #     {'year': 3, 'percentage': 0.85},
            >>> #     {'year': 4, 'percentage': 1.00}
            >>> # ]
        """
        schedules = {
            'aggressive': [
                {'year': 1, 'percentage': 0.50},
                {'year': 2, 'percentage': 0.85},
                {'year': 3, 'percentage': 1.00}
            ],
            'standard': [
                {'year': 1, 'percentage': 0.25},
                {'year': 2, 'percentage': 0.60},
                {'year': 3, 'percentage': 0.85},
                {'year': 4, 'percentage': 1.00}
            ],
            'conservative': [
                {'year': 1, 'percentage': 0.15},
                {'year': 2, 'percentage': 0.40},
                {'year': 3, 'percentage': 0.65},
                {'year': 4, 'percentage': 0.85},
                {'year': 5, 'percentage': 1.00}
            ]
        }
        
        return schedules.get(schedule_type, schedules['standard'])
    
    def calculate_synergy_npv(
        self,
        synergy_values: np.ndarray,
        discount_rate: float,
        periods_per_year: int = 12
    ) -> float:
        """
        Calculate NPV of synergy cash flows.
        
        Args:
            synergy_values: Array of synergy values per period
            discount_rate: Annual discount rate (decimal)
            periods_per_year: Number of periods per year
        
        Returns:
            NPV of synergies
        
        Example:
            >>> synergy_npv = engine.calculate_synergy_npv(synergies, 0.12, 12)
        """
        # Convert annual discount rate to per-period rate
        period_discount_rate = (1 + discount_rate) ** (1 / periods_per_year) - 1
        
        # Calculate discount factors
        periods = len(synergy_values)
        discount_factors = np.array([
            1 / (1 + period_discount_rate) ** t
            for t in range(periods)
        ])
        
        # Calculate NPV
        npv = np.sum(synergy_values * discount_factors)
        
        return npv
    
    def get_synergy_summary(
        self,
        synergy_models: List[Dict],
        periods: int,
        periods_per_year: int = 12
    ) -> Dict:
        """
        Get summary statistics for synergies.
        
        Args:
            synergy_models: List of synergy model dicts
            periods: Number of periods
            periods_per_year: Number of periods per year
        
        Returns:
            Dict with summary statistics
        
        Example:
            >>> summary = engine.get_synergy_summary(synergy_models, 240, 12)
            >>> # Returns: {
            >>> #     'total_target_value': 3500000,
            >>> #     'year_1_value': 875000,
            >>> #     'year_5_value': 3500000,
            >>> #     'categories': {...}
            >>> # }
        """
        # Calculate total synergies
        total_synergies = self.calculate_synergies(synergy_models, periods, periods_per_year)
        
        # Aggregate by year
        years = periods // periods_per_year
        annual_synergies = np.array([
            np.sum(total_synergies[y * periods_per_year:(y + 1) * periods_per_year])
            for y in range(years)
        ])
        
        # Calculate target values by category
        categories = {}
        for model in synergy_models:
            category = model['category']
            target_value = model['target_value']
            
            if category not in categories:
                categories[category] = 0
            categories[category] += target_value
        
        summary = {
            'total_target_value': sum(model['target_value'] for model in synergy_models),
            'year_1_value': annual_synergies[0] if len(annual_synergies) > 0 else 0,
            'year_5_value': annual_synergies[4] if len(annual_synergies) > 4 else annual_synergies[-1],
            'categories': categories,
            'annual_synergies': annual_synergies.tolist()
        }
        
        return summary

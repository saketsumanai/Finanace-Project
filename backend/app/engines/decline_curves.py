"""
Production decline curve models for oil and gas forecasting.

Implements three industry-standard decline curve models:
- Exponential: Q(t) = Q_i * e^(-D * t)
- Hyperbolic: Q(t) = Q_i / (1 + b * D_i * t)^(1/b)
- Harmonic: Q(t) = Q_i / (1 + D_i * t)
"""
from abc import ABC, abstractmethod
import numpy as np
from typing import Optional


class DeclineCurve(ABC):
    """Base class for production decline curves."""
    
    def __init__(self, initial_rate: float, decline_rate: float):
        """
        Initialize decline curve.
        
        Args:
            initial_rate: Initial production rate (Q_i)
            decline_rate: Decline rate (D or D_i)
        """
        if initial_rate <= 0:
            raise ValueError("Initial rate must be positive")
        if decline_rate < 0 or decline_rate > 1:
            raise ValueError("Decline rate must be between 0 and 1")
        
        self.initial_rate = initial_rate
        self.decline_rate = decline_rate
    
    @abstractmethod
    def forecast(self, periods: int) -> np.ndarray:
        """
        Generate production forecast for specified periods.
        
        Args:
            periods: Number of time periods to forecast
        
        Returns:
            Array of production rates
        """
        pass
    
    def forecast_cumulative(self, periods: int) -> np.ndarray:
        """
        Calculate cumulative production.
        
        Args:
            periods: Number of time periods
        
        Returns:
            Array of cumulative production
        """
        production = self.forecast(periods)
        return np.cumsum(production)


class ExponentialDecline(DeclineCurve):
    """
    Exponential decline curve model.
    
    Formula: Q(t) = Q_i * e^(-D * t)
    
    Characteristics:
    - Constant percentage decline
    - Most conservative forecast
    - Common for mature wells
    """
    
    def forecast(self, periods: int) -> np.ndarray:
        """
        Generate exponential decline forecast.
        
        Args:
            periods: Number of time periods to forecast
        
        Returns:
            Array of production rates
        """
        t = np.arange(0, periods)
        production = self.initial_rate * np.exp(-self.decline_rate * t)
        return production


class HyperbolicDecline(DeclineCurve):
    """
    Hyperbolic decline curve model.
    
    Formula: Q(t) = Q_i / (1 + b * D_i * t)^(1/b)
    
    Characteristics:
    - Variable decline rate
    - Most common in practice
    - Suitable for unconventional wells
    """
    
    def __init__(self, initial_rate: float, decline_rate: float, b_factor: float):
        """
        Initialize hyperbolic decline curve.
        
        Args:
            initial_rate: Initial production rate (Q_i)
            decline_rate: Initial decline rate (D_i)
            b_factor: Hyperbolic exponent (0 < b < 1)
        """
        super().__init__(initial_rate, decline_rate)
        
        if b_factor <= 0 or b_factor >= 1:
            raise ValueError("b_factor must be between 0 and 1")
        
        self.b_factor = b_factor
    
    def forecast(self, periods: int) -> np.ndarray:
        """
        Generate hyperbolic decline forecast.
        
        Args:
            periods: Number of time periods to forecast
        
        Returns:
            Array of production rates
        """
        t = np.arange(0, periods)
        denominator = 1 + self.b_factor * self.decline_rate * t
        production = self.initial_rate / np.power(denominator, 1 / self.b_factor)
        return production


class HarmonicDecline(DeclineCurve):
    """
    Harmonic decline curve model.
    
    Formula: Q(t) = Q_i / (1 + D_i * t)
    
    Characteristics:
    - Special case of hyperbolic (b = 1)
    - Slowest decline rate
    - Most optimistic forecast
    """
    
    def forecast(self, periods: int) -> np.ndarray:
        """
        Generate harmonic decline forecast.
        
        Args:
            periods: Number of time periods to forecast
        
        Returns:
            Array of production rates
        """
        t = np.arange(0, periods)
        production = self.initial_rate / (1 + self.decline_rate * t)
        return production


def create_decline_curve(
    curve_type: str,
    initial_rate: float,
    decline_rate: float,
    b_factor: Optional[float] = None
) -> DeclineCurve:
    """
    Factory function to create decline curve instances.
    
    Args:
        curve_type: Type of curve ('exponential', 'hyperbolic', 'harmonic')
        initial_rate: Initial production rate
        decline_rate: Decline rate
        b_factor: Hyperbolic exponent (required for hyperbolic)
    
    Returns:
        DeclineCurve instance
    
    Raises:
        ValueError: If curve_type is invalid or b_factor missing for hyperbolic
    """
    curve_type = curve_type.lower()
    
    if curve_type == 'exponential':
        return ExponentialDecline(initial_rate, decline_rate)
    elif curve_type == 'hyperbolic':
        if b_factor is None:
            raise ValueError("b_factor is required for hyperbolic decline")
        return HyperbolicDecline(initial_rate, decline_rate, b_factor)
    elif curve_type == 'harmonic':
        return HarmonicDecline(initial_rate, decline_rate)
    else:
        raise ValueError(f"Unknown curve type: {curve_type}")

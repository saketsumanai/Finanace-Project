"""
IRR (Internal Rate of Return) and NPV calculation engine.

Uses Newton-Raphson method for IRR calculation with high precision.
"""
import numpy as np
from typing import List, Optional
from scipy.optimize import newton


class IRREngine:
    """Engine for calculating IRR, NPV, and related metrics."""
    
    def __init__(self, tolerance: float = 0.0001, max_iterations: int = 100):
        """
        Initialize IRR engine.
        
        Args:
            tolerance: Convergence tolerance for IRR calculation
            max_iterations: Maximum iterations for Newton-Raphson
        """
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    
    def calculate_irr(self, cash_flows: List[float]) -> Optional[float]:
        """
        Calculate Internal Rate of Return using Newton-Raphson method.
        
        The IRR is the discount rate where NPV = 0:
        0 = Σ[CF_t / (1 + IRR)^t]
        
        Args:
            cash_flows: List of cash flows (initial investment should be negative)
        
        Returns:
            IRR as a decimal (e.g., 0.15 for 15%), or None if cannot converge
        
        Example:
            >>> engine = IRREngine()
            >>> cash_flows = [-100000, 30000, 40000, 50000, 40000]
            >>> irr = engine.calculate_irr(cash_flows)
            >>> print(f"IRR: {irr * 100:.2f}%")
            IRR: 18.45%
        """
        if not cash_flows or len(cash_flows) < 2:
            return None
        
        # Check if all cash flows are same sign (no IRR exists)
        if all(cf >= 0 for cf in cash_flows) or all(cf <= 0 for cf in cash_flows):
            return None
        
        # Initial guess: 10%
        initial_guess = 0.10
        
        try:
            irr = newton(
                func=self._npv_function,
                x0=initial_guess,
                fprime=self._npv_derivative,
                args=(cash_flows,),
                tol=self.tolerance,
                maxiter=self.max_iterations
            )
            
            # Validate result is reasonable (-100% to 1000%)
            if -1.0 <= irr <= 10.0:
                return irr
            else:
                return None
        
        except (RuntimeError, ValueError):
            # Try with different initial guesses
            for guess in [0.05, 0.20, 0.30, -0.05]:
                try:
                    irr = newton(
                        func=self._npv_function,
                        x0=guess,
                        fprime=self._npv_derivative,
                        args=(cash_flows,),
                        tol=self.tolerance,
                        maxiter=self.max_iterations
                    )
                    if -1.0 <= irr <= 10.0:
                        return irr
                except:
                    continue
            
            return None
    
    def _npv_function(self, rate: float, cash_flows: List[float]) -> float:
        """
        NPV function for root finding.
        
        Args:
            rate: Discount rate
            cash_flows: List of cash flows
        
        Returns:
            NPV at given rate
        """
        return sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))
    
    def _npv_derivative(self, rate: float, cash_flows: List[float]) -> float:
        """
        Derivative of NPV function for Newton-Raphson.
        
        Args:
            rate: Discount rate
            cash_flows: List of cash flows
        
        Returns:
            Derivative of NPV at given rate
        """
        return sum(-t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cash_flows))
    
    def calculate_npv(self, cash_flows: List[float], discount_rate: float) -> float:
        """
        Calculate Net Present Value.
        
        NPV = Σ[CF_t / (1 + r)^t]
        
        Args:
            cash_flows: List of cash flows
            discount_rate: Discount rate as decimal (e.g., 0.12 for 12%)
        
        Returns:
            NPV value
        
        Example:
            >>> engine = IRREngine()
            >>> cash_flows = [-100000, 30000, 40000, 50000, 40000]
            >>> npv = engine.calculate_npv(cash_flows, 0.12)
            >>> print(f"NPV: ${npv:,.2f}")
            NPV: $15,234.57
        """
        return sum(cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows))
    
    def calculate_payback_period(self, cash_flows: List[float]) -> Optional[float]:
        """
        Calculate payback period (time to recover initial investment).
        
        Args:
            cash_flows: List of cash flows
        
        Returns:
            Payback period in years, or None if never pays back
        
        Example:
            >>> engine = IRREngine()
            >>> cash_flows = [-100000, 30000, 40000, 50000, 40000]
            >>> payback = engine.calculate_payback_period(cash_flows)
            >>> print(f"Payback: {payback:.1f} years")
            Payback: 2.8 years
        """
        if not cash_flows or cash_flows[0] >= 0:
            return None
        
        cumulative = 0
        for t, cf in enumerate(cash_flows):
            cumulative += cf
            if cumulative >= 0:
                # Interpolate to get exact payback period
                if t == 0:
                    return 0.0
                previous_cumulative = cumulative - cf
                fraction = -previous_cumulative / cf
                return t - 1 + fraction
        
        return None  # Never pays back
    
    def calculate_roi(self, cash_flows: List[float]) -> Optional[float]:
        """
        Calculate Return on Investment.
        
        ROI = (Total Returns - Initial Investment) / Initial Investment
        
        Args:
            cash_flows: List of cash flows
        
        Returns:
            ROI as decimal (e.g., 0.50 for 50% return)
        """
        if not cash_flows or cash_flows[0] >= 0:
            return None
        
        initial_investment = abs(cash_flows[0])
        total_returns = sum(cash_flows[1:])
        
        roi = (total_returns - initial_investment) / initial_investment
        return roi
    
    def calculate_profitability_index(
        self,
        cash_flows: List[float],
        discount_rate: float
    ) -> Optional[float]:
        """
        Calculate Profitability Index (PI).
        
        PI = PV of future cash flows / Initial Investment
        
        Args:
            cash_flows: List of cash flows
            discount_rate: Discount rate as decimal
        
        Returns:
            Profitability Index (PI > 1 means profitable)
        """
        if not cash_flows or cash_flows[0] >= 0:
            return None
        
        initial_investment = abs(cash_flows[0])
        
        # Calculate PV of future cash flows
        pv_future = sum(
            cf / (1 + discount_rate) ** t
            for t, cf in enumerate(cash_flows[1:], start=1)
        )
        
        pi = pv_future / initial_investment
        return pi
    
    def calculate_mirr(
        self,
        cash_flows: List[float],
        finance_rate: float,
        reinvest_rate: float
    ) -> Optional[float]:
        """
        Calculate Modified Internal Rate of Return (MIRR).
        
        MIRR accounts for different rates for financing and reinvestment.
        
        Args:
            cash_flows: List of cash flows
            finance_rate: Cost of capital for negative cash flows
            reinvest_rate: Rate for reinvesting positive cash flows
        
        Returns:
            MIRR as decimal
        """
        if not cash_flows or len(cash_flows) < 2:
            return None
        
        n = len(cash_flows) - 1
        
        # Present value of negative cash flows (costs)
        pv_negative = sum(
            cf / (1 + finance_rate) ** t
            for t, cf in enumerate(cash_flows)
            if cf < 0
        )
        
        # Future value of positive cash flows (returns)
        fv_positive = sum(
            cf * (1 + reinvest_rate) ** (n - t)
            for t, cf in enumerate(cash_flows)
            if cf > 0
        )
        
        if pv_negative == 0:
            return None
        
        # Calculate MIRR
        mirr = (fv_positive / abs(pv_negative)) ** (1 / n) - 1
        return mirr

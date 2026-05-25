"""
AI-powered data generation service for creating realistic production and financial data.
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict
from decimal import Decimal


class DataGenerator:
    """Generate realistic oil & gas production and financial data."""
    
    def generate_production_data(
        self,
        project_id: int,
        months: int = 12,
        initial_oil: float = 1000.0,
        initial_gas: float = 5000.0,
        decline_rate: float = 0.15
    ) -> List[Dict]:
        """
        Generate realistic production data with decline.
        
        Args:
            project_id: Project ID
            months: Number of months to generate
            initial_oil: Initial oil production (bbl/day)
            initial_gas: Initial gas production (MCF/day)
            decline_rate: Annual decline rate (0.15 = 15%)
        
        Returns:
            List of production data dictionaries
        """
        data = []
        start_date = datetime.now() - timedelta(days=months * 30)
        
        # Convert annual decline to monthly
        monthly_decline = 1 - (1 - decline_rate) ** (1/12)
        
        current_oil = initial_oil
        current_gas = initial_gas
        
        for i in range(months):
            date = start_date + timedelta(days=i * 30)
            
            # Add some random variation (±5%)
            oil_variation = random.uniform(0.95, 1.05)
            gas_variation = random.uniform(0.95, 1.05)
            
            # Calculate water cut (increases over time)
            water_cut = 0.3 + (i / months) * 0.2  # 30% to 50%
            water_volume = current_oil * water_cut
            
            data.append({
                'project_id': project_id,
                'date': date.date(),
                'well_name': 'WELL-001',
                'oil_volume': round(current_oil * oil_variation, 2),
                'gas_volume': round(current_gas * gas_variation, 2),
                'water_volume': round(water_volume, 2),
                'oil_price': round(random.uniform(70, 85), 2),
                'gas_price': round(random.uniform(3.0, 4.5), 2),
            })
            
            # Apply decline
            current_oil *= (1 - monthly_decline)
            current_gas *= (1 - monthly_decline)
        
        return data
    
    def generate_financial_data(
        self,
        project_id: int,
        months: int = 12,
        initial_revenue: float = 500000.0,
        base_opex: float = 80000.0,
        initial_capex: float = 5000000.0
    ) -> List[Dict]:
        """
        Generate realistic financial data.
        
        Args:
            project_id: Project ID
            months: Number of months to generate
            initial_revenue: Initial monthly revenue
            base_opex: Base monthly OPEX
            initial_capex: Initial CAPEX (first month only)
        
        Returns:
            List of financial data dictionaries
        """
        data = []
        start_date = datetime.now() - timedelta(days=months * 30)
        
        current_revenue = initial_revenue
        monthly_opex_inflation = 1.0025  # ~3% annual
        
        for i in range(months):
            date = start_date + timedelta(days=i * 30)
            
            # Revenue declines with production
            revenue_decline = 0.985  # ~18% annual decline
            current_revenue *= revenue_decline
            
            # Add variation
            revenue = current_revenue * random.uniform(0.95, 1.05)
            
            # OPEX increases with inflation
            opex = base_opex * (monthly_opex_inflation ** i) * random.uniform(0.98, 1.02)
            
            # CAPEX only in first month and occasionally
            capex = initial_capex if i == 0 else (random.choice([0, 0, 0, 100000]) if i % 6 == 0 else 0)
            
            # Taxes (21% of profit)
            profit = max(0, revenue - opex)
            taxes = profit * 0.21
            
            # Royalties (12.5% of revenue)
            royalties = revenue * 0.125
            
            data.append({
                'project_id': project_id,
                'date': date.date(),
                'revenue': round(revenue, 2),
                'operating_cost': round(opex, 2),
                'opex': round(opex, 2),
                'capex': round(capex, 2),
                'taxes': round(taxes, 2),
                'royalties': round(royalties, 2),
            })
        
        return data
    
    def generate_smart_data(
        self,
        project_id: int,
        project_type: str = 'Acquisition',
        deal_size: float = 50000000.0
    ) -> Dict[str, List[Dict]]:
        """
        Generate smart, realistic data based on project characteristics.
        
        Uses AI-like logic to create appropriate data based on deal size and type.
        
        Args:
            project_id: Project ID
            project_type: Type of project (Acquisition, Divestiture, etc.)
            deal_size: Deal size in USD
        
        Returns:
            Dictionary with 'production' and 'financial' data
        """
        # Scale initial production based on deal size
        # Assume $50M deal = 1000 bbl/day
        scale_factor = deal_size / 50000000.0
        
        initial_oil = 1000 * scale_factor
        initial_gas = 5000 * scale_factor
        
        # Adjust decline rate based on project type
        decline_rates = {
            'Acquisition': 0.15,  # 15% - typical
            'Divestiture': 0.20,  # 20% - higher decline (why selling)
            'Joint Venture': 0.12,  # 12% - better assets
            'Farm-out': 0.18,  # 18% - moderate
        }
        decline_rate = decline_rates.get(project_type, 0.15)
        
        # Generate data
        production_data = self.generate_production_data(
            project_id=project_id,
            months=12,
            initial_oil=initial_oil,
            initial_gas=initial_gas,
            decline_rate=decline_rate
        )
        
        # Calculate initial revenue from production
        avg_oil_price = 75.0
        avg_gas_price = 3.5
        initial_revenue = (initial_oil * 30 * avg_oil_price + 
                          initial_gas * 30 * avg_gas_price / 1000)
        
        # OPEX scales with production
        base_opex = initial_oil * 30 * 2.5  # $2.50 per barrel
        
        # CAPEX is typically 10% of deal size
        initial_capex = deal_size * 0.10
        
        financial_data = self.generate_financial_data(
            project_id=project_id,
            months=12,
            initial_revenue=initial_revenue,
            base_opex=base_opex,
            initial_capex=initial_capex
        )
        
        return {
            'production': production_data,
            'financial': financial_data,
            'metadata': {
                'initial_oil_rate': initial_oil,
                'initial_gas_rate': initial_gas,
                'decline_rate': decline_rate,
                'months_generated': 12,
                'generation_method': 'AI-powered smart generation'
            }
        }


# Global instance
data_generator = DataGenerator()

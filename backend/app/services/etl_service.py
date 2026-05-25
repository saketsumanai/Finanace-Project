"""
ETL (Extract, Transform, Load) service for processing uploaded files.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
import os


class ETLService:
    """Service for extracting, transforming, and loading data from files."""
    
    def __init__(self):
        self.supported_formats = ['csv', 'xlsx']
    
    def extract_data(self, file_path: str, file_type: str) -> pd.DataFrame:
        """
        Extract data from uploaded file.
        
        Args:
            file_path: Path to the uploaded file
            file_type: Type of file (csv or xlsx)
        
        Returns:
            DataFrame with extracted data
        
        Raises:
            ValueError: If file format is not supported
        """
        file_extension = os.path.splitext(file_path)[1].lower().replace('.', '')
        
        if file_extension == 'csv':
            return pd.read_csv(file_path)
        elif file_extension in ['xlsx', 'xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def validate_production_data(self, df: pd.DataFrame) -> Tuple[bool, List[str], float]:
        """
        Validate production data schema and quality.
        
        Args:
            df: DataFrame with production data
        
        Returns:
            Tuple of (is_valid, errors, quality_score)
        """
        errors = []
        quality_score = 100.0
        
        # Required columns for production data
        required_columns = ['date', 'oil_production', 'gas_production']
        optional_columns = ['oil_price', 'gas_price']
        
        # Check for required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            quality_score -= 30
        
        if errors:
            return False, errors, quality_score
        
        # Check for missing values
        missing_pct = df[required_columns].isnull().sum().sum() / (len(df) * len(required_columns)) * 100
        if missing_pct > 0:
            errors.append(f"Missing values: {missing_pct:.1f}% of required data")
            quality_score -= min(missing_pct, 20)
        
        # Check for negative values
        numeric_cols = ['oil_production', 'gas_production']
        for col in numeric_cols:
            if col in df.columns:
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    errors.append(f"Found {negative_count} negative values in {col}")
                    quality_score -= 10
        
        # Check date format
        try:
            pd.to_datetime(df['date'])
        except Exception as e:
            errors.append(f"Invalid date format: {str(e)}")
            quality_score -= 20
        
        # Check for duplicates
        duplicate_count = df.duplicated(subset=['date']).sum()
        if duplicate_count > 0:
            errors.append(f"Found {duplicate_count} duplicate dates")
            quality_score -= 10
        
        is_valid = len(errors) == 0 or quality_score >= 70
        
        return is_valid, errors, max(0, quality_score)
    
    def validate_financial_data(self, df: pd.DataFrame) -> Tuple[bool, List[str], float]:
        """
        Validate financial data schema and quality.
        
        Args:
            df: DataFrame with financial data
        
        Returns:
            Tuple of (is_valid, errors, quality_score)
        """
        errors = []
        quality_score = 100.0
        
        # Required columns for financial data
        required_columns = ['date', 'revenue', 'opex']
        optional_columns = ['capex', 'loe', 'transportation_cost', 'ga_expense', 'ebitda']
        
        # Check for required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            quality_score -= 30
        
        if errors:
            return False, errors, quality_score
        
        # Check for missing values
        missing_pct = df[required_columns].isnull().sum().sum() / (len(df) * len(required_columns)) * 100
        if missing_pct > 0:
            errors.append(f"Missing values: {missing_pct:.1f}% of required data")
            quality_score -= min(missing_pct, 20)
        
        # Check date format
        try:
            pd.to_datetime(df['date'])
        except Exception as e:
            errors.append(f"Invalid date format: {str(e)}")
            quality_score -= 20
        
        # Check for duplicates
        duplicate_count = df.duplicated(subset=['date']).sum()
        if duplicate_count > 0:
            errors.append(f"Found {duplicate_count} duplicate dates")
            quality_score -= 10
        
        is_valid = len(errors) == 0 or quality_score >= 70
        
        return is_valid, errors, max(0, quality_score)
    
    def transform_production_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform and normalize production data.
        
        Args:
            df: Raw production data
        
        Returns:
            Transformed DataFrame
        """
        df = df.copy()
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Normalize column names
        column_mapping = {
            'Date': 'date',
            'Oil Production': 'oil_production',
            'Oil': 'oil_production',
            'Gas Production': 'gas_production',
            'Gas': 'gas_production',
            'Oil Price': 'oil_price',
            'Gas Price': 'gas_price',
        }
        df.rename(columns=column_mapping, inplace=True)
        
        # Convert to numeric, coercing errors
        numeric_columns = ['oil_production', 'gas_production', 'oil_price', 'gas_price']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with all NaN values
        df.dropna(how='all', subset=numeric_columns, inplace=True)
        
        # Sort by date
        df.sort_values('date', inplace=True)
        
        # Reset index
        df.reset_index(drop=True, inplace=True)
        
        return df
    
    def transform_financial_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform and normalize financial data.
        
        Args:
            df: Raw financial data
        
        Returns:
            Transformed DataFrame
        """
        df = df.copy()
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Normalize column names
        column_mapping = {
            'Date': 'date',
            'Revenue': 'revenue',
            'OPEX': 'opex',
            'Operating Expenses': 'opex',
            'CAPEX': 'capex',
            'Capital Expenditures': 'capex',
            'LOE': 'loe',
            'Lease Operating Expenses': 'loe',
            'Transportation': 'transportation_cost',
            'G&A': 'ga_expense',
            'EBITDA': 'ebitda',
        }
        df.rename(columns=column_mapping, inplace=True)
        
        # Convert to numeric
        numeric_columns = ['revenue', 'opex', 'capex', 'loe', 'transportation_cost', 'ga_expense', 'ebitda']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Calculate EBITDA if not provided
        if 'ebitda' not in df.columns and 'revenue' in df.columns and 'opex' in df.columns:
            df['ebitda'] = df['revenue'] - df['opex']
        
        # Remove rows with all NaN values
        df.dropna(how='all', subset=numeric_columns, inplace=True)
        
        # Sort by date
        df.sort_values('date', inplace=True)
        
        # Reset index
        df.reset_index(drop=True, inplace=True)
        
        return df
    
    def aggregate_by_period(self, df: pd.DataFrame, period: str = 'M') -> pd.DataFrame:
        """
        Aggregate data by time period.
        
        Args:
            df: DataFrame with date column
            period: Aggregation period ('D' for daily, 'M' for monthly, 'Q' for quarterly, 'Y' for yearly)
        
        Returns:
            Aggregated DataFrame
        """
        df = df.copy()
        df.set_index('date', inplace=True)
        
        # Aggregate numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        aggregated = df[numeric_columns].resample(period).sum()
        
        aggregated.reset_index(inplace=True)
        
        return aggregated
    
    def calculate_data_quality_score(self, df: pd.DataFrame, required_columns: List[str]) -> float:
        """
        Calculate overall data quality score.
        
        Args:
            df: DataFrame to evaluate
            required_columns: List of required column names
        
        Returns:
            Quality score between 0 and 100
        """
        score = 100.0
        
        # Completeness (40 points)
        missing_pct = df[required_columns].isnull().sum().sum() / (len(df) * len(required_columns)) * 100
        score -= min(missing_pct * 0.4, 40)
        
        # Consistency (30 points)
        duplicate_pct = df.duplicated().sum() / len(df) * 100
        score -= min(duplicate_pct * 0.3, 30)
        
        # Validity (30 points)
        # Check for negative values in numeric columns
        numeric_cols = df[required_columns].select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            negative_pct = (df[col] < 0).sum() / len(df) * 100
            score -= min(negative_pct * 0.1, 10)
        
        return max(0, score)

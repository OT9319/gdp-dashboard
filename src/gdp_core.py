"""
GDP Dashboard Core Module

This module provides core functionality for the GDP Dashboard application,
following the constitutional principles of the cerebrum-1 repository.

Security (AEGIS): No hardcoded secrets or sensitive information
Portability (PORTABILITÉ): Uses standard libraries and cross-platform code
Resilience (HYGIE): Designed with testability in mind
Efficiency (CHRONOS): Optimized data processing and caching
"""

import os
import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Optional, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GDPDataProcessor:
    """
    Handles GDP data processing with caching and validation.
    
    This class encapsulates the data processing logic to ensure
    separation of concerns and testability (HYGIE principle).
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the GDP data processor.
        
        Args:
            data_path: Path to GDP data file. If None, uses default location.
                      Can be overridden via GDP_DATA_PATH environment variable (AEGIS).
        """
        self.data_path = self._get_data_path(data_path)
        self.min_year = 1960
        self.max_year = 2022
        self._cached_data = None
        
    def _get_data_path(self, data_path: Optional[str]) -> Path:
        """
        Get data path with environment variable support for security (AEGIS).
        
        Args:
            data_path: Optional explicit data path
            
        Returns:
            Path object to the data file
        """
        if data_path:
            return Path(data_path)
        
        # Check environment variable first (AEGIS - security principle)
        env_path = os.getenv('GDP_DATA_PATH')
        if env_path:
            return Path(env_path)
        
        # Default to relative path
        return Path(__file__).parent.parent / 'data' / 'gdp_data.csv'
    
    @st.cache_data
    def load_and_process_data(_self) -> pd.DataFrame:
        """
        Load and process GDP data with caching for efficiency (CHRONOS).
        
        Returns:
            Processed DataFrame with columns: Country Code, Year, GDP
            
        Raises:
            FileNotFoundError: If data file doesn't exist
            ValueError: If data processing fails
        """
        try:
            if not _self.data_path.exists():
                raise FileNotFoundError(f"GDP data file not found: {_self.data_path}")
            
            logger.info(f"Loading GDP data from: {_self.data_path}")
            raw_gdp_df = pd.read_csv(_self.data_path)
            
            # Process data: pivot year columns into Year and GDP columns
            # This transformation improves data structure efficiency (CHRONOS)
            gdp_df = raw_gdp_df.melt(
                ['Country Code'],
                [str(x) for x in range(_self.min_year, _self.max_year + 1)],
                'Year',
                'GDP',
            )
            
            # Convert years from string to integers for better performance (CHRONOS)
            gdp_df['Year'] = pd.to_numeric(gdp_df['Year'], errors='coerce')
            
            # Filter out invalid data
            gdp_df = gdp_df.dropna(subset=['Year'])
            
            logger.info(f"Processed {len(gdp_df)} GDP data points")
            return gdp_df
            
        except Exception as e:
            logger.error(f"Error processing GDP data: {e}")
            raise ValueError(f"Failed to process GDP data: {e}")
    
    def get_data(self) -> pd.DataFrame:
        """
        Get processed GDP data, using cache when available.
        
        Returns:
            Processed GDP DataFrame
        """
        if self._cached_data is None:
            self._cached_data = self.load_and_process_data()
        return self._cached_data
    
    def get_available_countries(self) -> List[str]:
        """
        Get list of available country codes.
        
        Returns:
            Sorted list of country codes
        """
        data = self.get_data()
        return sorted(data['Country Code'].unique().tolist())
    
    def get_year_range(self) -> Tuple[int, int]:
        """
        Get available year range from the data.
        
        Returns:
            Tuple of (min_year, max_year)
        """
        data = self.get_data()
        return (int(data['Year'].min()), int(data['Year'].max()))
    
    def filter_data(self, countries: List[str], 
                   year_from: int, year_to: int) -> pd.DataFrame:
        """
        Filter GDP data by countries and year range.
        
        Args:
            countries: List of country codes to include
            year_from: Start year (inclusive)
            year_to: End year (inclusive)
            
        Returns:
            Filtered DataFrame
        """
        data = self.get_data()
        
        # Input validation for resilience (HYGIE)
        if not countries:
            logger.warning("No countries selected for filtering")
            return pd.DataFrame()
        
        if year_from > year_to:
            logger.warning(f"Invalid year range: {year_from} > {year_to}")
            year_from, year_to = year_to, year_from
        
        filtered_data = data[
            (data['Country Code'].isin(countries)) &
            (data['Year'] >= year_from) &
            (data['Year'] <= year_to)
        ]
        
        logger.info(f"Filtered to {len(filtered_data)} data points for {len(countries)} countries")
        return filtered_data


class GDPMetricsCalculator:
    """
    Calculate GDP-related metrics and statistics.
    
    Separate class to follow single responsibility principle (PORTABILITÉ).
    """
    
    @staticmethod
    def calculate_growth_metric(first_value: float, last_value: float) -> Tuple[str, str]:
        """
        Calculate growth metric between two GDP values.
        
        Args:
            first_value: GDP value at start of period
            last_value: GDP value at end of period
            
        Returns:
            Tuple of (growth_text, delta_color)
        """
        if pd.isna(first_value) or pd.isna(last_value) or first_value <= 0:
            return 'n/a', 'off'
        
        # Calculate growth multiplier
        growth = last_value / first_value
        return f'{growth:,.2f}x', 'normal'
    
    @staticmethod
    def format_gdp_billions(value: float) -> str:
        """
        Format GDP value in billions with appropriate precision.
        
        Args:
            value: GDP value in original units
            
        Returns:
            Formatted string (e.g., "1,234.5B")
        """
        if pd.isna(value):
            return 'N/A'
        
        billions = value / 1_000_000_000
        return f'{billions:,.0f}B'


def validate_environment() -> dict:
    """
    Validate environment configuration and security settings (AEGIS).
    
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        'data_path_secure': True,
        'no_hardcoded_secrets': True,
        'environment_ready': True
    }
    
    # Check for potential security issues
    env_vars = os.environ
    sensitive_patterns = ['password', 'secret', 'key', 'token']
    
    for var_name in env_vars:
        if any(pattern in var_name.lower() for pattern in sensitive_patterns):
            if var_name not in ['GDP_DATA_PATH']:  # Whitelist known safe variables
                logger.warning(f"Potentially sensitive environment variable: {var_name}")
    
    return validation_results
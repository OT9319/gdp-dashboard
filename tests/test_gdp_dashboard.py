"""Unit tests for GDP Dashboard functionality."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.gdp_dashboard import get_gdp_data, filter_gdp_data, calculate_growth_metrics


class TestGDPDashboard:
    """Test class for GDP Dashboard functions."""

    def test_get_gdp_data_returns_dataframe(self):
        """Test that get_gdp_data returns a DataFrame."""
        df = get_gdp_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_get_gdp_data_has_required_columns(self):
        """Test that the returned DataFrame has the required columns."""
        df = get_gdp_data()
        required_columns = ['Country Code', 'Year', 'GDP']
        for col in required_columns:
            assert col in df.columns

    def test_get_gdp_data_year_column_is_numeric(self):
        """Test that the Year column contains numeric values."""
        df = get_gdp_data()
        assert pd.api.types.is_numeric_dtype(df['Year'])

    def test_filter_gdp_data(self):
        """Test the filter_gdp_data function."""
        # Create a sample DataFrame
        data = {
            'Country Code': ['USA', 'CAN', 'MEX', 'USA', 'CAN', 'MEX'],
            'Year': [2020, 2020, 2020, 2021, 2021, 2021],
            'GDP': [1000, 500, 300, 1100, 550, 330]
        }
        df = pd.DataFrame(data)
        
        # Test filtering
        filtered = filter_gdp_data(df, ['USA', 'CAN'], 2020, 2021)
        
        # Should have 4 rows (USA and CAN for both years)
        assert len(filtered) == 4
        # Should only contain USA and CAN
        assert set(filtered['Country Code'].unique()) == {'USA', 'CAN'}
        # Should only contain years 2020 and 2021
        assert set(filtered['Year'].unique()) == {2020, 2021}

    def test_filter_gdp_data_empty_countries(self):
        """Test filter_gdp_data with empty countries list."""
        data = {
            'Country Code': ['USA', 'CAN'],
            'Year': [2020, 2020],
            'GDP': [1000, 500]
        }
        df = pd.DataFrame(data)
        
        filtered = filter_gdp_data(df, [], 2020, 2020)
        assert len(filtered) == 0

    def test_calculate_growth_metrics(self):
        """Test the calculate_growth_metrics function."""
        # Create sample data
        data = {
            'Country Code': ['USA', 'USA'],
            'Year': [2020, 2021],
            'GDP': [1000000000000, 1200000000000]  # 1T to 1.2T
        }
        df = pd.DataFrame(data)
        
        last_gdp, growth, delta_color = calculate_growth_metrics(df, 'USA', 2020, 2021)
        
        # GDP should be converted to billions
        assert last_gdp == 1200.0
        # Growth should be 1.2x
        assert growth == '1.20x'
        assert delta_color == 'normal'

    def test_calculate_growth_metrics_with_nan(self):
        """Test calculate_growth_metrics when first year data is NaN."""
        data = {
            'Country Code': ['USA', 'USA'],
            'Year': [2020, 2021],
            'GDP': [np.nan, 1200000000000]
        }
        df = pd.DataFrame(data)
        
        last_gdp, growth, delta_color = calculate_growth_metrics(df, 'USA', 2020, 2021)
        
        assert last_gdp == 1200.0
        assert growth == 'n/a'
        assert delta_color == 'off'

    def test_data_file_exists(self):
        """Test that the GDP data file exists."""
        data_file = Path(__file__).parent.parent / 'data/gdp_data.csv'
        assert data_file.exists(), f"GDP data file not found at {data_file}"
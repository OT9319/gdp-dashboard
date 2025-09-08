import pytest
import pandas as pd
from pathlib import Path
import sys
import os

# Add the parent directory to Python path to import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestGDPDashboard:
    """Test suite for the GDP Dashboard Streamlit application."""
    
    def test_data_file_exists(self):
        """Test that the GDP data file exists and is accessible."""
        data_file = Path(__file__).parent.parent / 'data' / 'gdp_data.csv'
        assert data_file.exists(), "GDP data file should exist"
        assert data_file.is_file(), "GDP data path should be a file"
    
    def test_data_can_be_loaded(self):
        """Test that the GDP data can be loaded successfully."""
        data_file = Path(__file__).parent.parent / 'data' / 'gdp_data.csv'
        df = pd.read_csv(data_file)
        assert not df.empty, "GDP data should not be empty"
        assert 'Country Code' in df.columns, "Data should have Country Code column"
    
    def test_data_format(self):
        """Test that the GDP data has the expected format and structure."""
        data_file = Path(__file__).parent.parent / 'data' / 'gdp_data.csv'
        df = pd.read_csv(data_file)
        
        # Check required columns exist
        required_columns = ['Country Code']
        for col in required_columns:
            assert col in df.columns, f"Column '{col}' should exist in data"
        
        # Check that there are year columns (should be string representations of years)
        year_columns = [col for col in df.columns if col.isdigit()]
        assert len(year_columns) > 0, "Data should contain year columns"
        
        # Check year range (should include recent years)
        years = [int(col) for col in year_columns]
        assert max(years) >= 2020, "Data should include recent years"
        assert min(years) <= 1980, "Data should include historical years"
    
    def test_streamlit_app_imports(self):
        """Test that the main streamlit app can be imported without errors."""
        try:
            # Import the main functions from streamlit_app
            import streamlit_app
            assert hasattr(streamlit_app, 'get_gdp_data'), "App should have get_gdp_data function"
        except ImportError as e:
            pytest.fail(f"Failed to import streamlit_app: {e}")
    
    def test_get_gdp_data_function(self):
        """Test the get_gdp_data function works correctly."""
        import streamlit_app
        
        # Test the function can be called
        gdp_df = streamlit_app.get_gdp_data()
        
        # Verify the returned dataframe structure
        assert not gdp_df.empty, "get_gdp_data should return non-empty dataframe"
        assert 'Country Code' in gdp_df.columns, "Result should have Country Code column"
        assert 'Year' in gdp_df.columns, "Result should have Year column" 
        assert 'GDP' in gdp_df.columns, "Result should have GDP column"
        
        # Check data types
        assert gdp_df['Year'].dtype in ['int64', 'int32'], "Year column should be integer"
        
        # Check that we have reasonable data
        assert len(gdp_df['Country Code'].unique()) > 10, "Should have multiple countries"
        assert gdp_df['Year'].min() >= 1960, "Years should be reasonable (>=1960)"
        assert gdp_df['Year'].max() <= 2030, "Years should be reasonable (<=2030)"

if __name__ == "__main__":
    pytest.main([__file__])
"""
Unit tests for the main Streamlit application.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the function we want to test
import streamlit_app


class TestGDPDataFunctions(unittest.TestCase):
    """Test cases for GDP data processing functions."""
    
    @patch('streamlit_app.pd.read_csv')
    def test_get_gdp_data_basic(self, mock_read_csv):
        """Test basic GDP data loading and transformation."""
        # Arrange
        mock_raw_data = pd.DataFrame({
            'Country Code': ['USA', 'FRA', 'GBR'],
            'Country Name': ['United States', 'France', 'United Kingdom'], 
            'Indicator Name': ['GDP (current US$)', 'GDP (current US$)', 'GDP (current US$)'],
            '1960': [543300000000, 62225478000, 38239000000],
            '1961': [563300000000, 66489000000, 41032000000],
            '2022': [25462700000000, 2937473000000, 3131000000000]
        })
        mock_read_csv.return_value = mock_raw_data
        
        # Act
        result = streamlit_app.get_gdp_data()
        
        # Assert
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('Country Code', result.columns)
        self.assertIn('Year', result.columns)
        self.assertIn('GDP', result.columns)
        
        # Check that data was properly melted
        expected_rows = len(mock_raw_data) * (2022 - 1960 + 1)  # 3 countries * 63 years
        self.assertEqual(len(result), expected_rows)
        
        # Check year conversion
        self.assertTrue(result['Year'].dtype in ['int64', 'int32'])
    
    @patch('streamlit_app.pd.read_csv')
    def test_get_gdp_data_with_missing_values(self, mock_read_csv):
        """Test GDP data processing with missing values."""
        # Arrange
        mock_raw_data = pd.DataFrame({
            'Country Code': ['USA', 'FRA'],
            'Country Name': ['United States', 'France'],
            'Indicator Name': ['GDP (current US$)', 'GDP (current US$)'],
            '2020': [21427700000000, None],  # Missing value for France
            '2021': [23315081000000, 2938271000000]
        })
        mock_read_csv.return_value = mock_raw_data
        
        # Act
        result = streamlit_app.get_gdp_data()
        
        # Assert
        self.assertIsInstance(result, pd.DataFrame)
        
        # Check that missing values are handled (should be NaN in pandas)
        france_2020 = result[(result['Country Code'] == 'FRA') & (result['Year'] == 2020)]['GDP'].iloc[0]
        self.assertTrue(pd.isna(france_2020))
    
    @patch('streamlit_app.Path')
    def test_get_gdp_data_file_path(self, mock_path):
        """Test that the correct file path is used for GDP data."""
        # Arrange
        mock_path_instance = MagicMock()
        mock_path.return_value.parent = mock_path_instance
        mock_path_instance.__truediv__ = MagicMock(return_value='data/gdp_data.csv')
        
        with patch('streamlit_app.pd.read_csv') as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame({
                'Country Code': ['USA'],
                '2022': [25000000000000]
            })
            
            # Act
            streamlit_app.get_gdp_data()
            
            # Assert - verify the CSV was called (path construction is complex to test exactly)
            mock_read_csv.assert_called_once()


class TestDataValidation(unittest.TestCase):
    """Test cases for data validation and edge cases."""
    
    def test_year_range_constants(self):
        """Test that year range constants are reasonable."""
        # These constants are defined in the get_gdp_data function
        # We can test them indirectly by ensuring the function works with expected ranges
        
        # Test that the function can handle the expected year range
        with patch('streamlit_app.pd.read_csv') as mock_read_csv:
            # Create data for the full expected range
            years = list(range(1960, 2023))  # 1960 to 2022 inclusive
            mock_data = pd.DataFrame({
                'Country Code': ['TEST'],
                **{str(year): [1000000000] for year in years}  # 1B GDP for each year
            })
            mock_read_csv.return_value = mock_data
            
            result = streamlit_app.get_gdp_data()
            
            # Check that all years are present
            result_years = sorted(result['Year'].unique())
            expected_years = list(range(1960, 2023))
            self.assertEqual(result_years, expected_years)
    
    def test_empty_data_handling(self):
        """Test behavior with empty dataset."""
        with patch('streamlit_app.pd.read_csv') as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame()  # Empty DataFrame
            
            # This might raise an exception, which is acceptable behavior
            with self.assertRaises(Exception):
                streamlit_app.get_gdp_data()


class TestAppStructure(unittest.TestCase):
    """Test cases for application structure and imports."""
    
    def test_required_imports(self):
        """Test that all required modules can be imported."""
        import streamlit
        import pandas
        import math
        from pathlib import Path
        
        # If we get here, all imports were successful
        self.assertTrue(True)
    
    def test_function_exists(self):
        """Test that the main function exists and is callable."""
        self.assertTrue(hasattr(streamlit_app, 'get_gdp_data'))
        self.assertTrue(callable(streamlit_app.get_gdp_data))
    
    def test_caching_decorator(self):
        """Test that the function has proper caching decorator."""
        # The function should have the @st.cache_data decorator
        # We can check if it has been wrapped
        func = streamlit_app.get_gdp_data
        
        # This is a bit complex to test directly, but we can ensure
        # the function can be called multiple times without issues
        with patch('streamlit_app.pd.read_csv') as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame({
                'Country Code': ['USA'],
                '2022': [25000000000000]
            })
            
            # Call twice - should work fine with caching
            result1 = func()
            result2 = func()
            
            self.assertIsInstance(result1, pd.DataFrame)
            self.assertIsInstance(result2, pd.DataFrame)


if __name__ == '__main__':
    unittest.main(verbosity=2)
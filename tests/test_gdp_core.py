"""
Test Suite for GDP Dashboard - Constitutional Compliance (HYGIE)

This test suite ensures the application follows constitutional principles:
- Security (AEGIS): Tests for secure configuration handling
- Portability (PORTABILITÉ): Tests for cross-platform compatibility  
- Resilience (HYGIE): Comprehensive error handling and edge cases
- Efficiency (CHRONOS): Performance and scalability validation
"""

import unittest
import tempfile
import os
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path to enable imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.gdp_core import GDPDataProcessor, GDPMetricsCalculator, validate_environment

class TestGDPDataProcessor(unittest.TestCase):
    """Test cases for GDPDataProcessor class."""
    
    def setUp(self):
        """Set up test fixtures with sample data."""
        # Create temporary test data
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_path = Path(self.temp_dir) / 'test_gdp.csv'
        
        # Sample GDP data for testing - create full year range
        test_data = {
            'Country Code': ['USA', 'CHN']
        }
        
        # Add year columns from 1960-2022 (matching the processor's expected range)
        for year in range(1960, 2023):
            if year in [2020, 2021, 2022]:
                # Use realistic values for test years
                test_data[str(year)] = {
                    2020: [21430000000000, 14723000000000],
                    2021: [22996000000000, 17730000000000], 
                    2022: [25000000000000, 18000000000000]
                }[year]
            else:
                # Generate reasonable values for other years
                base_usa = 10000000000000  # 10 trillion base for USA
                base_chn = 5000000000000   # 5 trillion base for China
                growth_usa = (year - 1960) * 200000000000  # ~200B growth per year
                growth_chn = (year - 1960) * 150000000000  # ~150B growth per year
                test_data[str(year)] = [base_usa + growth_usa, base_chn + growth_chn]
        pd.DataFrame(test_data).to_csv(self.test_data_path, index=False)
        
        self.processor = GDPDataProcessor(str(self.test_data_path))
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.test_data_path.exists():
            self.test_data_path.unlink()
        os.rmdir(self.temp_dir)
    
    def test_data_loading_success(self):
        """Test successful data loading and processing (HYGIE)."""
        data = self.processor.get_data()
        
        # Verify data structure
        self.assertIsInstance(data, pd.DataFrame)
        self.assertIn('Country Code', data.columns)
        self.assertIn('Year', data.columns)
        self.assertIn('GDP', data.columns)
        
        # Verify data types
        self.assertTrue(pd.api.types.is_numeric_dtype(data['Year']))
        
    def test_data_loading_file_not_found(self):
        """Test handling of missing data file (HYGIE)."""
        processor = GDPDataProcessor('/nonexistent/path/file.csv')
        
        with self.assertRaises(ValueError):
            processor.load_and_process_data()
    
    def test_environment_variable_path(self):
        """Test environment variable configuration (AEGIS)."""
        # Set environment variable
        os.environ['GDP_DATA_PATH'] = str(self.test_data_path)
        
        try:
            processor = GDPDataProcessor()
            data = processor.get_data()
            self.assertIsInstance(data, pd.DataFrame)
            self.assertGreater(len(data), 0)
        finally:
            # Clean up environment
            if 'GDP_DATA_PATH' in os.environ:
                del os.environ['GDP_DATA_PATH']
    
    def test_get_available_countries(self):
        """Test country list retrieval (PORTABILITÉ)."""
        countries = self.processor.get_available_countries()
        
        self.assertIsInstance(countries, list)
        self.assertIn('USA', countries)
        self.assertIn('CHN', countries)
        self.assertTrue(all(isinstance(c, str) for c in countries))
    
    def test_get_year_range(self):
        """Test year range retrieval (CHRONOS)."""
        min_year, max_year = self.processor.get_year_range()
        
        self.assertIsInstance(min_year, int)
        self.assertIsInstance(max_year, int)
        self.assertGreaterEqual(max_year, min_year)
    
    def test_filter_data_valid_inputs(self):
        """Test data filtering with valid inputs (HYGIE)."""
        filtered = self.processor.filter_data(['USA'], 2020, 2021)
        
        self.assertIsInstance(filtered, pd.DataFrame)
        self.assertEqual(set(filtered['Country Code'].unique()), {'USA'})
        self.assertTrue(all(2020 <= year <= 2021 for year in filtered['Year']))
    
    def test_filter_data_empty_countries(self):
        """Test data filtering with empty country list (HYGIE)."""
        filtered = self.processor.filter_data([], 2020, 2021)
        
        self.assertIsInstance(filtered, pd.DataFrame)
        self.assertEqual(len(filtered), 0)
    
    def test_filter_data_invalid_year_range(self):
        """Test data filtering with invalid year range (HYGIE)."""
        # Should handle reversed year range gracefully
        filtered = self.processor.filter_data(['USA'], 2021, 2020)
        
        self.assertIsInstance(filtered, pd.DataFrame)
        # Should contain data for both years despite reversed input
        self.assertTrue(len(filtered) > 0)


class TestGDPMetricsCalculator(unittest.TestCase):
    """Test cases for GDPMetricsCalculator class."""
    
    def setUp(self):
        """Set up test calculator."""
        self.calculator = GDPMetricsCalculator()
    
    def test_calculate_growth_metric_valid_values(self):
        """Test growth calculation with valid values (CHRONOS)."""
        growth_text, delta_color = self.calculator.calculate_growth_metric(1000, 1500)
        
        self.assertEqual(growth_text, '1.50x')
        self.assertEqual(delta_color, 'normal')
    
    def test_calculate_growth_metric_nan_values(self):
        """Test growth calculation with NaN values (HYGIE)."""
        growth_text, delta_color = self.calculator.calculate_growth_metric(float('nan'), 1500)
        
        self.assertEqual(growth_text, 'n/a')
        self.assertEqual(delta_color, 'off')
    
    def test_calculate_growth_metric_zero_first_value(self):
        """Test growth calculation with zero first value (HYGIE)."""
        growth_text, delta_color = self.calculator.calculate_growth_metric(0, 1500)
        
        self.assertEqual(growth_text, 'n/a')
        self.assertEqual(delta_color, 'off')
    
    def test_format_gdp_billions_valid_value(self):
        """Test GDP formatting with valid value (PORTABILITÉ)."""
        formatted = self.calculator.format_gdp_billions(1500000000000)  # 1.5 trillion
        
        self.assertEqual(formatted, '1,500B')
    
    def test_format_gdp_billions_nan_value(self):
        """Test GDP formatting with NaN value (HYGIE)."""
        formatted = self.calculator.format_gdp_billions(float('nan'))
        
        self.assertEqual(formatted, 'N/A')
    
    def test_format_gdp_billions_zero_value(self):
        """Test GDP formatting with zero value (HYGIE)."""
        formatted = self.calculator.format_gdp_billions(0)
        
        self.assertEqual(formatted, '0B')


class TestSecurityValidation(unittest.TestCase):
    """Test cases for security validation (AEGIS)."""
    
    def test_validate_environment_basic(self):
        """Test basic environment validation."""
        results = validate_environment()
        
        self.assertIsInstance(results, dict)
        self.assertIn('data_path_secure', results)
        self.assertIn('no_hardcoded_secrets', results)
        self.assertIn('environment_ready', results)
    
    def test_validate_environment_with_safe_variables(self):
        """Test environment validation with safe variables."""
        # Set a safe environment variable
        os.environ['GDP_DATA_PATH'] = '/safe/path/data.csv'
        
        try:
            results = validate_environment()
            self.assertTrue(results['environment_ready'])
        finally:
            if 'GDP_DATA_PATH' in os.environ:
                del os.environ['GDP_DATA_PATH']


class TestPerformanceAndEfficiency(unittest.TestCase):
    """Test cases for performance optimization (CHRONOS)."""
    
    def setUp(self):
        """Set up performance test fixtures."""
        # Create larger test dataset for performance testing
        self.temp_dir = tempfile.mkdtemp()
        self.large_data_path = Path(self.temp_dir) / 'large_test_gdp.csv'
        
        # Generate test data with multiple countries and full year range
        countries = ['USA', 'CHN', 'GER', 'JPN', 'GBR', 'FRA', 'IND', 'BRA', 'CAN', 'AUS']
        
        data = []
        for country in countries:
            row = {'Country Code': country}
            # Generate values for full year range (1960-2022)
            for year in range(1960, 2023):
                # Generate mock GDP values based on country and year
                base_value = 1000000000000 + hash(country) % 5000000000000
                growth = (year - 1960) * 50000000000
                row[str(year)] = base_value + growth
            data.append(row)
        
        pd.DataFrame(data).to_csv(self.large_data_path, index=False)
        self.processor = GDPDataProcessor(str(self.large_data_path))
    
    def tearDown(self):
        """Clean up performance test fixtures."""
        if self.large_data_path.exists():
            self.large_data_path.unlink()
        os.rmdir(self.temp_dir)
    
    def test_data_processing_efficiency(self):
        """Test that data processing completes in reasonable time (CHRONOS)."""
        import time
        
        start_time = time.time()
        data = self.processor.get_data()
        end_time = time.time()
        
        # Should process in less than 2 seconds for test data
        self.assertLess(end_time - start_time, 2.0)
        
        # Verify data quality
        self.assertGreater(len(data), 0)
        self.assertEqual(len(data['Country Code'].unique()), 10)  # 10 countries
    
    def test_filtering_efficiency(self):
        """Test that data filtering is efficient (CHRONOS)."""
        import time
        
        start_time = time.time()
        filtered = self.processor.filter_data(['USA', 'CHN', 'GER'], 2010, 2020)
        end_time = time.time()
        
        # Should filter in less than 1 second
        self.assertLess(end_time - start_time, 1.0)
        
        # Verify filtering results
        self.assertEqual(set(filtered['Country Code'].unique()), {'USA', 'CHN', 'GER'})
        self.assertTrue(all(2010 <= year <= 2020 for year in filtered['Year']))


if __name__ == '__main__':
    # Run all tests with detailed output
    unittest.main(verbosity=2)
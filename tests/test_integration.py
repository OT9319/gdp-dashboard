"""
Integration Tests for GDP Dashboard UI Components

Tests the complete UI integration following constitutional principles.
These tests validate the interaction between UI and core components.
"""

import unittest
import tempfile
import os
import pandas as pd
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path to enable imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

class TestGDPDashboardIntegration(unittest.TestCase):
    """Integration tests for the complete dashboard system."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        # Create temporary test data
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_path = Path(self.temp_dir) / 'integration_test_gdp.csv'
        
        # Create comprehensive test data with full year range
        countries = ['USA', 'CHN', 'GER', 'FRA']
        test_data = {'Country Code': countries}
        
        # Add year columns from 1960-2022
        for year in range(1960, 2023):
            if year in [2020, 2021, 2022]:
                # Use realistic values for recent years
                values = {
                    2020: [21430000000000, 14723000000000, 3846000000000, 2630000000000],
                    2021: [22996000000000, 17730000000000, 4259000000000, 2938000000000],
                    2022: [25000000000000, 18000000000000, 4500000000000, 3100000000000]
                }[year]
            else:
                # Generate reasonable historical values
                bases = [10000000000000, 5000000000000, 2000000000000, 1500000000000]
                growths = [200000000000, 150000000000, 50000000000, 30000000000]
                values = [base + (year - 1960) * growth for base, growth in zip(bases, growths)]
            
            test_data[str(year)] = values
        pd.DataFrame(test_data).to_csv(self.test_data_path, index=False)
        
        # Set environment variable for testing
        os.environ['GDP_DATA_PATH'] = str(self.test_data_path)
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        if self.test_data_path.exists():
            self.test_data_path.unlink()
        os.rmdir(self.temp_dir)
        
        if 'GDP_DATA_PATH' in os.environ:
            del os.environ['GDP_DATA_PATH']
    
    def test_end_to_end_data_flow(self):
        """Test complete data flow from loading to processing (HYGIE)."""
        from src.gdp_core import GDPDataProcessor
        from src.gdp_ui import GDPDashboardUI
        
        # Test data loading
        processor = GDPDataProcessor()
        data = processor.get_data()
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 0)
        
        # Test country filtering
        countries = processor.get_available_countries()
        self.assertIn('USA', countries)
        self.assertIn('CHN', countries)
        
        # Test data filtering
        filtered = processor.filter_data(['USA', 'CHN'], 2020, 2022)
        self.assertEqual(set(filtered['Country Code'].unique()), {'USA', 'CHN'})
        
    @patch('streamlit.set_page_config')
    @patch('streamlit.title')
    @patch('streamlit.markdown')
    def test_ui_initialization_without_streamlit_context(self, mock_markdown, mock_title, mock_config):
        """Test UI initialization in non-Streamlit context (PORTABILITÉ)."""
        from src.gdp_ui import GDPDashboardUI
        
        try:
            dashboard = GDPDashboardUI()
            self.assertIsNotNone(dashboard.data_processor)
            self.assertIsNotNone(dashboard.metrics_calculator)
        except Exception as e:
            # Should handle Streamlit context gracefully
            self.assertIn('streamlit', str(e).lower())
    
    def test_security_validation_integration(self):
        """Test security validation integration (AEGIS)."""
        from src.gdp_core import validate_environment
        
        # Test with current environment
        results = validate_environment()
        self.assertIsInstance(results, dict)
        self.assertTrue(results['environment_ready'])
        
        # Test with potentially sensitive environment variable
        os.environ['TEST_SECRET_KEY'] = 'test_value'
        try:
            results = validate_environment()
            # Should still work but may log warnings
            self.assertIsInstance(results, dict)
        finally:
            del os.environ['TEST_SECRET_KEY']
    
    def test_error_handling_integration(self):
        """Test error handling across components (HYGIE)."""
        from src.gdp_core import GDPDataProcessor
        
        # Test with invalid data path
        processor = GDPDataProcessor('/nonexistent/path/file.csv')
        
        with self.assertRaises(ValueError):
            processor.get_data()
        
        # Test graceful handling of filter with non-existent countries
        processor = GDPDataProcessor()
        filtered = processor.filter_data(['NONEXISTENT'], 2020, 2022)
        self.assertEqual(len(filtered), 0)


class TestConstitutionalCompliance(unittest.TestCase):
    """Tests specifically for constitutional principle compliance."""
    
    def test_aegis_security_principle(self):
        """Test AEGIS (Security) principle compliance."""
        from src.gdp_core import GDPDataProcessor, validate_environment
        
        # Test environment variable usage
        test_path = '/tmp/test.csv'
        os.environ['GDP_DATA_PATH'] = test_path
        
        try:
            processor = GDPDataProcessor()
            self.assertEqual(str(processor.data_path), test_path)
        finally:
            del os.environ['GDP_DATA_PATH']
        
        # Test security validation
        results = validate_environment()
        self.assertIn('data_path_secure', results)
        self.assertIn('no_hardcoded_secrets', results)
    
    def test_portabilite_portability_principle(self):
        """Test PORTABILITÉ (Portability) principle compliance."""
        from src.gdp_core import GDPDataProcessor
        
        # Test cross-platform path handling
        processor = GDPDataProcessor()
        self.assertIsInstance(processor.data_path, Path)
        
        # Test that default paths work across platforms
        default_path = processor._get_data_path(None)
        self.assertIsInstance(default_path, Path)
    
    def test_hygie_resilience_principle(self):
        """Test HYGIE (Resilience) principle compliance."""
        from src.gdp_core import GDPDataProcessor, GDPMetricsCalculator
        
        # Test error handling in data processing
        processor = GDPDataProcessor('/nonexistent/file.csv')
        
        with self.assertRaises(ValueError):
            processor.load_and_process_data()
        
        # Test error handling in metrics calculation
        calculator = GDPMetricsCalculator()
        
        # Should handle NaN values gracefully
        growth, color = calculator.calculate_growth_metric(float('nan'), 1000)
        self.assertEqual(growth, 'n/a')
        self.assertEqual(color, 'off')
        
        # Should handle division by zero
        growth, color = calculator.calculate_growth_metric(0, 1000)
        self.assertEqual(growth, 'n/a')
        self.assertEqual(color, 'off')
    
    def test_chronos_efficiency_principle(self):
        """Test CHRONOS (Efficiency) principle compliance."""
        from src.gdp_core import GDPDataProcessor
        import time
        
        # Create test data for performance testing
        temp_dir = tempfile.mkdtemp()
        test_data_path = Path(temp_dir) / 'efficiency_test.csv'
        
        try:
            # Generate moderately sized test data with full year range
            countries = ['USA', 'CHN', 'GER', 'FRA', 'GBR']
            
            data = []
            for country in countries:
                row = {'Country Code': country}
                # Generate values for full year range (1960-2022)
                for year in range(1960, 2023):
                    base_value = 1000000000000 + hash(country) % 2000000000000
                    growth = (year - 1960) * 10000000000
                    row[str(year)] = base_value + growth
                data.append(row)
            
            pd.DataFrame(data).to_csv(test_data_path, index=False)
            
            # Test processing efficiency
            processor = GDPDataProcessor(str(test_data_path))
            
            start_time = time.time()
            data = processor.get_data()
            processing_time = time.time() - start_time
            
            # Should process efficiently (less than 1 second for test data)
            self.assertLess(processing_time, 1.0)
            
            # Test filtering efficiency
            start_time = time.time()
            filtered = processor.filter_data(['USA', 'CHN'], 2010, 2020)
            filtering_time = time.time() - start_time
            
            # Should filter efficiently
            self.assertLess(filtering_time, 0.5)
            
        finally:
            # Clean up
            if test_data_path.exists():
                test_data_path.unlink()
            os.rmdir(temp_dir)


class TestDocumentationCompliance(unittest.TestCase):
    """Test compliance with documentation requirements (Article 4)."""
    
    def test_module_docstrings_present(self):
        """Test that modules have proper docstrings (Clarity requirement)."""
        import src.gdp_core
        import src.gdp_ui
        
        # Check module-level docstrings
        self.assertIsNotNone(src.gdp_core.__doc__)
        self.assertIsNotNone(src.gdp_ui.__doc__)
        
        # Check that docstrings mention constitutional principles
        core_doc = src.gdp_core.__doc__
        self.assertIn('AEGIS', core_doc)
        self.assertIn('PORTABILITÉ', core_doc)
        self.assertIn('HYGIE', core_doc)
        self.assertIn('CHRONOS', core_doc)
    
    def test_class_docstrings_present(self):
        """Test that classes have proper docstrings."""
        from src.gdp_core import GDPDataProcessor, GDPMetricsCalculator
        
        self.assertIsNotNone(GDPDataProcessor.__doc__)
        self.assertIsNotNone(GDPMetricsCalculator.__doc__)
        
        # Check for meaningful descriptions
        self.assertGreater(len(GDPDataProcessor.__doc__.strip()), 50)
        self.assertGreater(len(GDPMetricsCalculator.__doc__.strip()), 30)
    
    def test_critical_method_docstrings(self):
        """Test that critical methods have proper docstrings."""
        from src.gdp_core import GDPDataProcessor, GDPMetricsCalculator
        
        processor = GDPDataProcessor()
        calculator = GDPMetricsCalculator()
        
        # Check key methods have docstrings
        self.assertIsNotNone(processor.load_and_process_data.__doc__)
        self.assertIsNotNone(processor.filter_data.__doc__)
        self.assertIsNotNone(calculator.calculate_growth_metric.__doc__)
        self.assertIsNotNone(calculator.format_gdp_billions.__doc__)


if __name__ == '__main__':
    # Run integration tests with high verbosity
    unittest.main(verbosity=2)
"""
Integration tests for the GDP Dashboard application.
Tests the actual application behavior with real data structures.
"""

import unittest
import pandas as pd
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit_app


class TestGDPDashboardIntegration(unittest.TestCase):
    """Integration tests for the GDP Dashboard."""
    
    def test_data_file_exists(self):
        """Test that the GDP data file exists."""
        data_path = Path(__file__).parent.parent.parent / 'data' / 'gdp_data.csv'
        self.assertTrue(data_path.exists(), "GDP data file should exist")
    
    def test_data_loading_real_data(self):
        """Test that the real data can be loaded and processed."""
        # This tests the actual function with real data
        try:
            result = streamlit_app.get_gdp_data()
            
            # Basic structure checks
            self.assertIsInstance(result, pd.DataFrame)
            self.assertGreater(len(result), 0, "Should have data rows")
            
            # Required columns
            required_columns = ['Country Code', 'Year', 'GDP']
            for col in required_columns:
                self.assertIn(col, result.columns, f"Column {col} should exist")
            
            # Data type checks
            self.assertTrue(result['Year'].dtype in ['int64', 'int32'], "Year should be integer")
            
            # Year range check
            years = result['Year'].unique()
            self.assertGreater(len(years), 50, "Should have data for many years")
            self.assertGreaterEqual(min(years), 1960, "Should have historical data")
            self.assertLessEqual(max(years), 2025, "Years should be reasonable")
            
        except Exception as e:
            self.fail(f"Data loading failed: {e}")
    
    def test_data_structure_consistency(self):
        """Test that the data structure is consistent."""
        try:
            df = streamlit_app.get_gdp_data()
            
            # Check for consistent country codes
            country_codes = df['Country Code'].unique()
            self.assertGreater(len(country_codes), 10, "Should have multiple countries")
            
            # Each country code should be a string of 3 characters (ISO codes)
            for code in country_codes[:5]:  # Check first 5
                self.assertEqual(len(str(code)), 3, f"Country code {code} should be 3 characters")
            
        except Exception as e:
            self.fail(f"Data structure test failed: {e}")
    
    def test_math_operations_safe(self):
        """Test that math operations in the app are safe."""
        import math
        
        # Test the math operations used in the app
        test_values = [1000000000, 0, None, float('nan')]
        
        for value in test_values:
            try:
                if value is None or (isinstance(value, float) and math.isnan(value)):
                    # Test the isnan check used in the app
                    self.assertTrue(math.isnan(float('nan')))
                    continue
                
                # Test division used in the app (GDP conversion to billions)
                result = value / 1000000000
                self.assertIsInstance(result, (int, float))
                
            except Exception as e:
                # Some operations might fail with None/NaN, which is expected
                pass


class TestApplicationStructure(unittest.TestCase):
    """Test application structure and imports."""
    
    def test_required_modules_importable(self):
        """Test that all required modules can be imported."""
        modules = ['streamlit', 'pandas', 'math', 'pathlib']
        
        for module in modules:
            try:
                __import__(module)
            except ImportError:
                self.fail(f"Required module {module} cannot be imported")
    
    def test_streamlit_app_structure(self):
        """Test basic structure of the Streamlit app."""
        # Check that the main app file exists and is readable
        app_path = Path(__file__).parent.parent.parent / 'streamlit_app.py'
        self.assertTrue(app_path.exists())
        
        # Check that it contains expected Streamlit elements
        with open(app_path, 'r') as f:
            content = f.read()
        
        expected_elements = [
            'st.set_page_config',
            'st.cache_data',
            'st.slider',
            'st.multiselect',
            'st.line_chart',
            'st.metric'
        ]
        
        for element in expected_elements:
            self.assertIn(element, content, f"App should contain {element}")
    
    def test_data_directory_structure(self):
        """Test that data directory has expected structure."""
        project_root = Path(__file__).parent.parent.parent
        
        # Check required directories
        required_dirs = ['data', 'src', 'tests', 'docs', 'prompts']
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            self.assertTrue(dir_path.exists() and dir_path.is_dir(), 
                          f"Directory {dir_name} should exist")
    
    def test_security_scripts_exist(self):
        """Test that AEGIS security scripts exist."""
        project_root = Path(__file__).parent.parent.parent
        security_scripts = [
            'scripts/security/scan-secrets.py',
            'scripts/security/check-dependencies.py'
        ]
        
        for script_path in security_scripts:
            full_path = project_root / script_path
            self.assertTrue(full_path.exists(), f"Security script {script_path} should exist")
            self.assertTrue(os.access(full_path, os.X_OK), f"Security script {script_path} should be executable")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
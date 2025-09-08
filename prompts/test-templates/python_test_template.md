# HYGIE - Test Templates and Guidelines
# =====================================

## Python Unit Test Template

```python
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from your_module import YourClass, your_function


class TestYourFunction(unittest.TestCase):
    """Test cases for your_function."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    def test_function_basic_case(self):
        """Test basic functionality of your_function."""
        # Arrange
        input_data = "test_input"
        expected_output = "expected_result"
        
        # Act
        result = your_function(input_data)
        
        # Assert
        self.assertEqual(result, expected_output)
    
    def test_function_edge_case(self):
        """Test edge case handling."""
        # Arrange
        edge_input = None
        
        # Act & Assert
        with self.assertRaises(ValueError):
            your_function(edge_input)
    
    @patch('your_module.external_dependency')
    def test_function_with_mock(self, mock_dependency):
        """Test function behavior with mocked dependencies."""
        # Arrange
        mock_dependency.return_value = "mocked_result"
        input_data = "test_input"
        
        # Act
        result = your_function(input_data)
        
        # Assert
        self.assertTrue(mock_dependency.called)
        self.assertEqual(result, "expected_result_with_mock")


class TestYourClass(unittest.TestCase):
    """Test cases for YourClass."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.instance = YourClass()
    
    def test_initialization(self):
        """Test class initialization."""
        self.assertIsNotNone(self.instance)
        # Add specific initialization tests
    
    def test_method_behavior(self):
        """Test method behavior."""
        # Arrange
        expected_result = "expected"
        
        # Act
        result = self.instance.your_method()
        
        # Assert
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
```

## Streamlit Test Template

```python
import streamlit as st
import pandas as pd
import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# For testing Streamlit apps
from streamlit.testing.v1 import AppTest


class TestStreamlitApp(unittest.TestCase):
    """Test cases for Streamlit application."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = AppTest.from_file("streamlit_app.py")
    
    def test_app_loads(self):
        """Test that the app loads without errors."""
        self.app.run()
        assert not self.app.exception
    
    def test_title_display(self):
        """Test that the title is displayed correctly."""
        self.app.run()
        # Check if title is present in the app
        # Note: Specific assertions depend on your app structure
    
    @patch('pandas.read_csv')
    def test_data_loading(self, mock_read_csv):
        """Test data loading functionality."""
        # Mock CSV data
        mock_data = pd.DataFrame({
            'Country Code': ['USA', 'FRA'],
            '2020': [21000000000000, 2600000000000],
            '2021': [22000000000000, 2700000000000]
        })
        mock_read_csv.return_value = mock_data
        
        self.app.run()
        
        # Assert data is processed correctly
        assert not self.app.exception
        mock_read_csv.assert_called_once()


if __name__ == '__main__':
    unittest.main()
```

## Test Guidelines (HYGIE Principles)

### 1. Test Structure
- **Arrange**: Set up test data and conditions
- **Act**: Execute the function/method being tested
- **Assert**: Verify the results match expectations

### 2. Test Categories
- **Unit Tests**: Test individual functions/methods in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows

### 3. Best Practices
- **One assertion per test**: Each test should verify one specific behavior
- **Descriptive names**: Test names should clearly describe what is being tested
- **Independent tests**: Tests should not depend on other tests
- **Mock external dependencies**: Use mocks for databases, APIs, file systems

### 4. Coverage Goals
- **Minimum 80% code coverage**
- **All public functions should have tests**
- **Edge cases and error conditions should be tested**

### 5. Test Data
- Use **fixtures** for reusable test data
- Create **separate test data files** for complex scenarios
- **Clean up** test data after each test

## Quick Test Commands

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/unit/test_example.py

# Run tests with verbose output
python -m pytest tests/ -v
```
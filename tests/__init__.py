"""
Test configuration and utilities for HYGIE testing framework.
"""

import sys
from pathlib import Path
import unittest

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / 'src'))


class BaseTestCase(unittest.TestCase):
    """Base test case with common utilities."""
    
    def setUp(self):
        """Set up common test fixtures."""
        self.project_root = PROJECT_ROOT
        self.test_data_path = self.project_root / 'tests' / 'data'
    
    def assertFileExists(self, file_path):
        """Assert that a file exists."""
        path = Path(file_path)
        self.assertTrue(path.exists(), f"File does not exist: {path}")
    
    def assertDirectoryExists(self, dir_path):
        """Assert that a directory exists."""
        path = Path(dir_path)
        self.assertTrue(path.is_dir(), f"Directory does not exist: {path}")


def run_tests():
    """Run all tests in the tests directory."""
    loader = unittest.TestLoader()
    start_dir = PROJECT_ROOT / 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
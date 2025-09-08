"""
GDP Dashboard - Constitutional Application Entry Point

This is the main entry point for the GDP Dashboard application,
restructured according to the constitutional principles of cerebrum-1.

Security (AEGIS): Environment-based configuration and security validation
Portability (PORTABILITÉ): Cross-platform compatibility and open standards
Resilience (HYGIE): Comprehensive error handling and logging
Efficiency (CHRONOS): Optimized imports and initialization
"""

import sys
import logging
from pathlib import Path

# Add src directory to path for imports (PORTABILITÉ)
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Constitutional imports
from src.gdp_ui import GDPDashboardUI
from src.gdp_core import validate_environment

# Configure logging according to constitutional clarity principle
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Main application entry point following constitutional principles.
    
    This function initializes and runs the GDP Dashboard application
    with proper security validation and error handling.
    """
    try:
        # Constitutional security validation (AEGIS)
        logger.info("Performing constitutional security validation...")
        validation_results = validate_environment()
        
        if not validation_results.get('environment_ready', False):
            logger.error("Environment validation failed - security requirements not met")
            return
        
        logger.info("Security validation passed - proceeding with application startup")
        
        # Initialize and run the dashboard (HYGIE - resilient initialization)
        logger.info("Initializing GDP Dashboard UI...")
        dashboard = GDPDashboardUI()
        
        logger.info("Starting GDP Dashboard application...")
        dashboard.run()
        
    except ImportError as e:
        logger.error(f"Module import failed: {e}")
        logger.error("Please ensure all dependencies are installed: pip install -r requirements.txt")
        
    except Exception as e:
        logger.error(f"Critical application error: {e}")
        logger.error("Application failed to start - check logs for details")

if __name__ == "__main__":
    main()
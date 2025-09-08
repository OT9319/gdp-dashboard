"""
GDP Dashboard - Main Entry Point

This is the main entry point for the GDP Dashboard application.
Constitution Compliance: Follows constitutional requirements for structure,
security, and maintainability.

The application logic has been moved to src/gdp_dashboard.py for better
organization and constitutional compliance (Article 4 - Structure).
"""

import sys
from pathlib import Path

# Add src directory to Python path to import our application module
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

try:
    # Import and run the main application
    from gdp_dashboard import main
    
    # Execute the main application
    main()
    
except ImportError as e:
    import streamlit as st
    st.error(f"❌ Failed to import application modules: {e}")
    st.info("Please ensure all application files are properly installed.")
except Exception as e:
    import streamlit as st
    st.error(f"❌ Application startup error: {e}")
    st.info("Please check the application logs for more details.")

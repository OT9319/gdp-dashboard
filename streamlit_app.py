"""
GDP Dashboard - Legacy Compatibility Entry Point

This file maintains backwards compatibility while integrating with the new
constitutional structure of the cerebrum-1 repository.

MIGRATION NOTICE:
This application has been restructured according to constitutional principles.
The new modular structure provides:
- Enhanced security (AEGIS)
- Better portability (PORTABILITÉ) 
- Improved resilience (HYGIE)
- Optimized efficiency (CHRONOS)

For development, consider using the new entry point: src/main.py
"""

import sys
from pathlib import Path
import logging

# Configure logging for transparency (Constitutional Article 4 - Clarity)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src directory to Python path for constitutional imports (PORTABILITÉ)
src_path = Path(__file__).parent / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    # Import constitutional components
    from src.gdp_ui import GDPDashboardUI
    from src.gdp_core import validate_environment
    
    # Constitutional security validation (AEGIS)
    logger.info("🏛️ Initializing GDP Dashboard with constitutional compliance...")
    
    validation_results = validate_environment()
    if not validation_results.get('environment_ready', True):
        logger.warning("⚠️ Environment validation issues detected")
    
    # Initialize and run the constitutional dashboard (HYGIE)
    dashboard = GDPDashboardUI()
    dashboard.run()
    
    logger.info("✅ GDP Dashboard running under constitutional governance")
    
except ImportError as e:
    logger.error(f"❌ Failed to import constitutional modules: {e}")
    logger.info("🔄 Falling back to legacy implementation...")
    
    # Legacy fallback implementation for backwards compatibility
    import streamlit as st
    import pandas as pd
    import math
    
    # Set the title and favicon that appear in the Browser's tab bar.
    st.set_page_config(
        page_title='GDP Dashboard (Legacy Mode)',
        page_icon=':earth_americas:',
    )
    
    st.warning("⚠️ Running in legacy mode. Constitutional modules not available.")
    st.info("Install dependencies with: `pip install -r requirements.txt`")
    
    @st.cache_data
    def get_gdp_data():
        """Legacy GDP data loading function."""
        DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
        raw_gdp_df = pd.read_csv(DATA_FILENAME)
        
        MIN_YEAR = 1960
        MAX_YEAR = 2022
        
        gdp_df = raw_gdp_df.melt(
            ['Country Code'],
            [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
            'Year',
            'GDP',
        )
        
        gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
        return gdp_df
    
    # Legacy UI implementation
    st.title(':earth_americas: GDP Dashboard (Legacy Mode)')
    st.markdown("Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website.")
    
    gdp_df = get_gdp_data()
    
    min_value = gdp_df['Year'].min()
    max_value = gdp_df['Year'].max()
    
    from_year, to_year = st.slider(
        'Which years are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value])
    
    countries = gdp_df['Country Code'].unique()
    
    selected_countries = st.multiselect(
        'Which countries would you like to view?',
        countries,
        ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])
    
    if not selected_countries:
        st.warning("Select at least one country")
    else:
        filtered_gdp_df = gdp_df[
            (gdp_df['Country Code'].isin(selected_countries))
            & (gdp_df['Year'] <= to_year)
            & (from_year <= gdp_df['Year'])
        ]
        
        st.header('GDP over time', divider='gray')
        st.line_chart(
            filtered_gdp_df,
            x='Year',
            y='GDP',
            color='Country Code',
        )
        
        st.header(f'GDP in {to_year}', divider='gray')
        
        first_year = gdp_df[gdp_df['Year'] == from_year]
        last_year = gdp_df[gdp_df['Year'] == to_year]
        
        cols = st.columns(4)
        
        for i, country in enumerate(selected_countries):
            col = cols[i % len(cols)]
            
            with col:
                first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
                last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
                
                if math.isnan(first_gdp):
                    growth = 'n/a'
                    delta_color = 'off'
                else:
                    growth = f'{last_gdp / first_gdp:,.2f}x'
                    delta_color = 'normal'
                
                st.metric(
                    label=f'{country} GDP',
                    value=f'{last_gdp:,.0f}B',
                    delta=growth,
                    delta_color=delta_color
                )

except Exception as e:
    logger.error(f"❌ Critical error in application: {e}")
    import streamlit as st
    st.error("🚨 Application failed to load. Please refresh the page or check the logs.")

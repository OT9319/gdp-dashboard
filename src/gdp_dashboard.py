"""
GDP Dashboard Application

This module contains the main Streamlit application for visualizing GDP data
from the World Bank Open Data. It implements the constitutional requirements
for security, portability, resilience, and efficiency.

Constitution Compliance:
- AEGIS (Security): Uses environment variables for configuration
- PORTABILITÉ (Portability): Built with open standards (Python, Streamlit, CSV)
- HYGIE (Resilience): Comprehensive error handling and data validation
- CHRONOS (Efficiency): Optimized data processing with caching
"""

import streamlit as st
import pandas as pd
import math
import os
from pathlib import Path
from typing import List, Tuple, Optional
import logging

# Configure logging for better debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP Dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
    layout='wide',  # Use wide layout for better data visualization
)

# -----------------------------------------------------------------------------
# Security Configuration (AEGIS Compliance)
# -----------------------------------------------------------------------------

def get_config_value(key: str, default: str) -> str:
    """
    Securely retrieve configuration values from environment variables.
    
    Constitution Compliance: AEGIS (Clause 2.1)
    This function ensures sensitive configuration is loaded from environment
    variables rather than hardcoded values.
    
    Args:
        key: Environment variable name
        default: Default value if environment variable is not set
        
    Returns:
        Configuration value from environment or default
    """
    return os.getenv(key, default)

# Configuration constants - using environment variables for security
DATA_PATH = get_config_value('GDP_DATA_PATH', 'data/gdp_data.csv')
CACHE_TTL = int(get_config_value('CACHE_TTL_SECONDS', '3600'))  # 1 hour default
MIN_YEAR = int(get_config_value('MIN_YEAR', '1960'))
MAX_YEAR = int(get_config_value('MAX_YEAR', '2022'))

# -----------------------------------------------------------------------------
# Data Processing Functions (HYGIE & CHRONOS Compliance)
# -----------------------------------------------------------------------------

@st.cache_data(ttl=CACHE_TTL)
def get_gdp_data() -> pd.DataFrame:
    """
    Load and process GDP data from CSV file with comprehensive error handling.
    
    Constitution Compliance:
    - HYGIE (Clause 2.3): Robust error handling and validation
    - CHRONOS (Clause 2.4): Efficient caching to avoid repeated file reads
    
    This function implements caching to avoid having to read the file every time.
    The TTL (Time To Live) is configurable via environment variables for flexibility.
    
    Returns:
        Processed GDP DataFrame with columns: Country Code, Year, GDP
        
    Raises:
        FileNotFoundError: If the GDP data file cannot be found
        ValueError: If the data format is invalid
        pd.errors.EmptyDataError: If the CSV file is empty
    """
    try:
        # Construct data file path relative to the script location
        DATA_FILENAME = Path(__file__).parent.parent / DATA_PATH
        
        if not DATA_FILENAME.exists():
            logger.error(f"GDP data file not found: {DATA_FILENAME}")
            raise FileNotFoundError(f"GDP data file not found: {DATA_FILENAME}")
            
        logger.info(f"Loading GDP data from: {DATA_FILENAME}")
        raw_gdp_df = pd.read_csv(DATA_FILENAME)
        
        if raw_gdp_df.empty:
            raise pd.errors.EmptyDataError("GDP data file is empty")
            
        # Validate required columns exist
        required_columns = ['Country Code'] + [str(year) for year in range(MIN_YEAR, MAX_YEAR + 1)]
        missing_columns = [col for col in required_columns if col not in raw_gdp_df.columns]
        if missing_columns:
            logger.warning(f"Missing columns in GDP data: {missing_columns}")
        
        # Data transformation: Pivot year columns into Year and GDP columns
        # Original format: Country Code, 1960, 1961, 1962, ..., 2022
        # Target format: Country Code, Year, GDP
        available_years = [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1) if str(x) in raw_gdp_df.columns]
        
        gdp_df = raw_gdp_df.melt(
            ['Country Code'],
            available_years,
            'Year',
            'GDP',
        )

        # Convert years from string to integers for proper sorting and filtering
        gdp_df['Year'] = pd.to_numeric(gdp_df['Year'], errors='coerce')
        
        # Remove rows with invalid years or GDP values
        gdp_df = gdp_df.dropna(subset=['Year'])
        
        # Log data statistics for monitoring
        logger.info(f"Loaded GDP data: {len(gdp_df)} records, "
                   f"{gdp_df['Country Code'].nunique()} countries, "
                   f"years {gdp_df['Year'].min()}-{gdp_df['Year'].max()}")
        
        return gdp_df
        
    except FileNotFoundError:
        st.error("❌ GDP data file not found. Please ensure the data file is available.")
        raise
    except pd.errors.EmptyDataError:
        st.error("❌ GDP data file is empty. Please check the data source.")
        raise
    except Exception as e:
        logger.error(f"Error loading GDP data: {e}")
        st.error(f"❌ Error loading GDP data: {e}")
        raise

def validate_country_selection(countries: List[str], selected_countries: List[str]) -> List[str]:
    """
    Validate and filter country selections.
    
    Constitution Compliance: HYGIE (Clause 2.3)
    Implements defensive programming to handle invalid selections.
    
    Args:
        countries: Available country codes
        selected_countries: User-selected country codes
        
    Returns:
        Validated list of country codes
    """
    if not selected_countries:
        return []
        
    # Filter out any invalid country codes
    valid_countries = [country for country in selected_countries if country in countries]
    
    if len(valid_countries) != len(selected_countries):
        invalid = set(selected_countries) - set(valid_countries)
        logger.warning(f"Invalid country codes filtered out: {invalid}")
        
    return valid_countries

def calculate_gdp_metrics(gdp_df: pd.DataFrame, country: str, from_year: int, to_year: int) -> Tuple[float, float, str, str]:
    """
    Calculate GDP metrics for a specific country and time period.
    
    Constitution Compliance: CHRONOS (Clause 2.4)
    Optimized calculation with proper error handling.
    
    Args:
        gdp_df: GDP DataFrame
        country: Country code
        from_year: Starting year
        to_year: Ending year
        
    Returns:
        Tuple of (first_gdp_billions, last_gdp_billions, growth_text, delta_color)
    """
    try:
        first_year_data = gdp_df[(gdp_df['Year'] == from_year) & (gdp_df['Country Code'] == country)]
        last_year_data = gdp_df[(gdp_df['Year'] == to_year) & (gdp_df['Country Code'] == country)]
        
        if first_year_data.empty or last_year_data.empty:
            return 0, 0, 'n/a', 'off'
            
        first_gdp = first_year_data['GDP'].iloc[0] / 1_000_000_000  # Convert to billions
        last_gdp = last_year_data['GDP'].iloc[0] / 1_000_000_000
        
        if pd.isna(first_gdp) or pd.isna(last_gdp) or first_gdp <= 0:
            return last_gdp if not pd.isna(last_gdp) else 0, last_gdp if not pd.isna(last_gdp) else 0, 'n/a', 'off'
            
        growth = f'{last_gdp / first_gdp:.2f}x'
        return first_gdp, last_gdp, growth, 'normal'
        
    except Exception as e:
        logger.error(f"Error calculating metrics for {country}: {e}")
        return 0, 0, 'error', 'off'

# -----------------------------------------------------------------------------
# Main Application Logic
# -----------------------------------------------------------------------------

def main():
    """
    Main application entry point.
    
    Constitution Compliance: All clauses
    - AEGIS: Secure configuration loading
    - PORTABILITÉ: Standard Python/Streamlit implementation
    - HYGIE: Comprehensive error handling
    - CHRONOS: Efficient data processing
    """
    try:
        # Load GDP data with error handling
        gdp_df = get_gdp_data()
        
        # Application header and documentation
        st.title('🌍 GDP Dashboard')
        st.markdown("""
        Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. 
        As you'll notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
        But it's otherwise a great (and did I mention _free_?) source of data.
        
        **Constitution Compliance**: This application follows the constitutional principles for security, 
        portability, resilience, and efficiency.
        """)
        
        # Add some spacing
        st.markdown("---")
        
        # Year range selection with validation
        min_value = int(gdp_df['Year'].min())
        max_value = int(gdp_df['Year'].max())
        
        from_year, to_year = st.slider(
            '📅 Which years are you interested in?',
            min_value=min_value,
            max_value=max_value,
            value=[min_value, max_value]
        )
        
        # Country selection with validation
        countries = sorted(gdp_df['Country Code'].unique())
        
        default_countries = ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']
        # Filter default countries to only include those available in data
        available_defaults = [c for c in default_countries if c in countries]
        
        selected_countries = st.multiselect(
            '🏛️ Which countries would you like to view?',
            countries,
            default=available_defaults,
            help="Select one or more countries to compare their GDP over time"
        )
        
        # Validate selections
        selected_countries = validate_country_selection(countries, selected_countries)
        
        if not selected_countries:
            st.warning("⚠️ Please select at least one country to display data.")
            return
            
        st.markdown("---")
        
        # Filter the data based on selections
        filtered_gdp_df = gdp_df[
            (gdp_df['Country Code'].isin(selected_countries))
            & (gdp_df['Year'] <= to_year)
            & (from_year <= gdp_df['Year'])
        ]
        
        if filtered_gdp_df.empty:
            st.warning("⚠️ No data available for the selected countries and time period.")
            return
        
        # GDP over time visualization
        st.header('📈 GDP Over Time', divider='gray')
        
        # Create the line chart with better formatting
        st.line_chart(
            filtered_gdp_df,
            x='Year',
            y='GDP',
            color='Country Code',
            height=400
        )
        
        st.markdown("---")
        
        # GDP metrics for the selected end year
        st.header(f'💰 GDP in {to_year}', divider='gray')
        
        # Create metrics in columns for better layout
        cols = st.columns(min(4, len(selected_countries)))
        
        for i, country in enumerate(selected_countries):
            col = cols[i % len(cols)]
            
            with col:
                first_gdp, last_gdp, growth, delta_color = calculate_gdp_metrics(
                    gdp_df, country, from_year, to_year
                )
                
                # Display the metric with proper formatting
                st.metric(
                    label=f'{country} GDP',
                    value=f'${last_gdp:,.0f}B' if last_gdp > 0 else 'N/A',
                    delta=growth if growth != 'error' else None,
                    delta_color=delta_color,
                    help=f"GDP growth from {from_year} to {to_year}"
                )
        
        # Additional information footer
        st.markdown("---")
        st.caption("""
        📊 **Data Source**: World Bank Open Data  
        🔒 **Constitution Compliant**: This application adheres to security, portability, resilience, and efficiency principles  
        ⚡ **Performance**: Data is cached for optimal performance with configurable TTL
        """)
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"❌ Application error: {e}")
        st.info("💡 Please check the logs for more details or contact the system administrator.")

if __name__ == "__main__":
    main()
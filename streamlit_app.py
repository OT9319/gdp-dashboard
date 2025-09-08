import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data() -> pd.DataFrame:
    """
    Load and process GDP data from CSV file.
    
    This function loads GDP data from the World Bank Open Data CSV file,
    transforms it from wide format (years as columns) to long format
    (year as a column), and returns a clean DataFrame for analysis.
    
    The function uses Streamlit's caching to avoid reloading the data
    on every app interaction, improving performance (CHRONOS principle).
    
    Returns:
        pd.DataFrame: Processed GDP data with columns:
            - Country Code (str): ISO 3-letter country codes
            - Year (int): Year of GDP measurement
            - GDP (float): GDP value in current US dollars
    
    Raises:
        FileNotFoundError: If the GDP data CSV file is not found.
        pd.errors.ParserError: If the CSV file cannot be parsed.
    
    Example:
        >>> df = get_gdp_data()
        >>> print(df.head())
        Country Code  Year           GDP
        0          ABW  1960  5.422000e+07
        1          ABW  1961  6.000000e+07
        
    Note:
        Data source: World Bank Open Data (https://data.worldbank.org/)
        Coverage: 1960-2022 (may have missing values for some countries/years)
    """
    # PORTABILITÉ: Use pathlib.Path for cross-platform file path handling
    data_filename = Path(__file__).parent / 'data' / 'gdp_data.csv'
    
    # AEGIS: Validate that the data file exists before processing
    if not data_filename.exists():
        raise FileNotFoundError(
            f"GDP data file not found: {data_filename}. "
            f"Please ensure the data file is available."
        )
    
    try:
        # CHRONOS: Load data efficiently with pandas
        raw_gdp_df = pd.read_csv(data_filename)
    except Exception as e:
        raise pd.errors.ParserError(f"Failed to parse GDP data file: {e}")
    
    # Data processing constants
    MIN_YEAR = 1960
    MAX_YEAR = 2022
    
    # CHRONOS: Transform data from wide to long format efficiently
    # Original format: Country Code, Country Name, 1960, 1961, ..., 2022  
    # Target format: Country Code, Year, GDP
    year_columns = [str(year) for year in range(MIN_YEAR, MAX_YEAR + 1)]
    
    # AEGIS: Validate that required columns exist
    required_columns = ['Country Code'] + year_columns
    missing_columns = [col for col in required_columns if col not in raw_gdp_df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in GDP data: {missing_columns}")
    
    # Melt the DataFrame to convert year columns to rows
    gdp_df = raw_gdp_df.melt(
        id_vars=['Country Code'],
        value_vars=year_columns,
        var_name='Year',
        value_name='GDP'
    )
    
    # CHRONOS: Convert year column to integer for better performance and memory usage
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'], errors='coerce')
    
    # CHRONOS: Convert GDP to numeric, handling any non-numeric values gracefully
    gdp_df['GDP'] = pd.to_numeric(gdp_df['GDP'], errors='coerce')
    
    # AEGIS: Validate data integrity - ensure we have reasonable data
    if len(gdp_df) == 0:
        raise ValueError("No valid GDP data found after processing")
    
    return gdp_df

def calculate_gdp_growth_rate(initial_gdp: float, final_gdp: float) -> str:
    """
    Calculate GDP growth rate between two periods.
    
    Args:
        initial_gdp (float): GDP value for the initial period.
        final_gdp (float): GDP value for the final period.
    
    Returns:
        str: Formatted growth rate string (e.g., "2.15x") or "n/a" for invalid data.
    
    Note:
        CHRONOS: Uses math.isnan for efficient NaN checking.
        AEGIS: Handles division by zero and invalid inputs safely.
    """
    # AEGIS: Handle invalid inputs safely
    if math.isnan(initial_gdp) or math.isnan(final_gdp) or initial_gdp <= 0:
        return 'n/a'
    
    # CHRONOS: Simple division for growth rate calculation
    growth_rate = final_gdp / initial_gdp
    return f'{growth_rate:,.2f}x'


def format_gdp_value(gdp_value: float) -> str:
    """
    Format GDP value in billions with proper formatting.
    
    Args:
        gdp_value (float): GDP value in current US dollars.
    
    Returns:
        str: Formatted GDP string in billions (e.g., "21,427B").
        
    Note:
        CHRONOS: Efficient conversion using simple division.
        AEGIS: Handles NaN and invalid values gracefully.
    """
    if math.isnan(gdp_value):
        return "N/A"
    
    # CHRONOS: Convert to billions for better readability
    gdp_billions = gdp_value / 1_000_000_000
    return f'{gdp_billions:,.0f}B'

# CHRONOS: Load data once and cache for performance
gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

# Add some spacing
''
''

# AEGIS: Validate data bounds to prevent invalid slider values
min_value = int(gdp_df['Year'].min()) if not gdp_df.empty else 1960
max_value = int(gdp_df['Year'].max()) if not gdp_df.empty else 2022

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value]
)

# CHRONOS: Get unique countries efficiently
countries = sorted(gdp_df['Country Code'].unique()) if not gdp_df.empty else []

# AEGIS: Validate that we have countries to display
if not countries:
    st.error("No country data available. Please check the data file.")
    st.stop()

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']
)

# HYGIE: Provide user feedback when no countries are selected
if not selected_countries:
    st.warning("Please select at least one country to view data.")

''
''
''

# CHRONOS: Efficient data filtering using pandas boolean indexing
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries)) &
    (gdp_df['Year'] >= from_year) & 
    (gdp_df['Year'] <= to_year)
].copy()  # CHRONOS: Copy to avoid SettingWithCopyWarning

st.header('GDP over time', divider='gray')

''

# Display chart only if we have data to show
if not filtered_gdp_df.empty:
    st.line_chart(
        filtered_gdp_df,
        x='Year',
        y='GDP',
        color='Country Code',
    )
else:
    st.info("No data available for the selected countries and year range.")

''
''

# CHRONOS: Pre-filter data for specific years to improve performance
first_year_data = gdp_df[gdp_df['Year'] == from_year] if not gdp_df.empty else pd.DataFrame()
last_year_data = gdp_df[gdp_df['Year'] == to_year] if not gdp_df.empty else pd.DataFrame()

st.header(f'GDP in {to_year}', divider='gray')

''

# Display metrics only if we have selected countries
if selected_countries and not first_year_data.empty and not last_year_data.empty:
    # CHRONOS: Use columns for efficient layout
    cols = st.columns(4)
    
    for i, country in enumerate(selected_countries):
        col = cols[i % len(cols)]
        
        with col:
            # AEGIS: Safe data access with error handling
            try:
                # Get GDP data for the country in both years
                first_country_data = first_year_data[first_year_data['Country Code'] == country]
                last_country_data = last_year_data[last_year_data['Country Code'] == country]
                
                if first_country_data.empty or last_country_data.empty:
                    # Handle missing data gracefully
                    st.metric(
                        label=f'{country} GDP',
                        value="No data",
                        delta="n/a",
                        delta_color='off'
                    )
                    continue
                
                first_gdp = first_country_data['GDP'].iloc[0]
                last_gdp = last_country_data['GDP'].iloc[0]
                
                # CHRONOS: Use our helper functions for consistent formatting
                formatted_gdp = format_gdp_value(last_gdp)
                growth_rate = calculate_gdp_growth_rate(first_gdp, last_gdp)
                
                # Determine delta color based on growth
                delta_color = 'off' if growth_rate == 'n/a' else 'normal'
                
                st.metric(
                    label=f'{country} GDP',
                    value=formatted_gdp,
                    delta=growth_rate,
                    delta_color=delta_color
                )
                
            except (IndexError, KeyError, ValueError) as e:
                # AEGIS: Log error and show user-friendly message
                st.metric(
                    label=f'{country} GDP',
                    value="Error",
                    delta="n/a",
                    delta_color='off'
                )
else:
    st.info("Select countries to see GDP metrics for the selected year range.")

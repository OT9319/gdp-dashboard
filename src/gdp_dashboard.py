"""GDP Dashboard core functionality."""

import pandas as pd
import math
from pathlib import Path
from typing import List, Tuple

def get_gdp_data() -> pd.DataFrame:
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    
    Returns:
        pd.DataFrame: GDP data with columns Country Code, Year, GDP
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent.parent / 'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df


def filter_gdp_data(gdp_df: pd.DataFrame, countries: List[str], from_year: int, to_year: int) -> pd.DataFrame:
    """Filter GDP data by countries and years.
    
    Args:
        gdp_df: The GDP dataframe
        countries: List of country codes to include
        from_year: Start year (inclusive)
        to_year: End year (inclusive)
        
    Returns:
        pd.DataFrame: Filtered GDP data
    """
    return gdp_df[
        (gdp_df['Country Code'].isin(countries))
        & (gdp_df['Year'] <= to_year)
        & (from_year <= gdp_df['Year'])
    ]


def calculate_growth_metrics(gdp_df: pd.DataFrame, country: str, from_year: int, to_year: int) -> Tuple[float, str, str]:
    """Calculate growth metrics for a specific country.
    
    Args:
        gdp_df: The GDP dataframe
        country: Country code
        from_year: Start year
        to_year: End year
        
    Returns:
        Tuple of (last_gdp_in_billions, growth_text, delta_color)
    """
    first_year_data = gdp_df[gdp_df['Year'] == from_year]
    last_year_data = gdp_df[gdp_df['Year'] == to_year]
    
    first_gdp = first_year_data[first_year_data['Country Code'] == country]['GDP'].iat[0] / 1000000000
    last_gdp = last_year_data[last_year_data['Country Code'] == country]['GDP'].iat[0] / 1000000000

    if math.isnan(first_gdp):
        growth = 'n/a'
        delta_color = 'off'
    else:
        growth = f'{last_gdp / first_gdp:,.2f}x'
        delta_color = 'normal'
    
    return last_gdp, growth, delta_color
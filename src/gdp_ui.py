"""
GDP Dashboard UI Components

This module contains the Streamlit UI components for the GDP Dashboard,
organized according to constitutional principles.

Security (AEGIS): Environment-based configuration support
Portability (PORTABILITÉ): Framework-agnostic UI logic
Resilience (HYGIE): Error handling and validation
Efficiency (CHRONOS): Optimized rendering and state management
"""

import streamlit as st
import pandas as pd
import math
from typing import List, Tuple, Optional
import logging
from src.gdp_core import GDPDataProcessor, GDPMetricsCalculator

logger = logging.getLogger(__name__)

class GDPDashboardUI:
    """
    Main UI class for the GDP Dashboard application.
    
    Encapsulates all UI logic to maintain separation of concerns (PORTABILITÉ).
    """
    
    def __init__(self):
        """Initialize the dashboard UI components."""
        self.data_processor = GDPDataProcessor()
        self.metrics_calculator = GDPMetricsCalculator()
        self._initialize_page_config()
    
    def _initialize_page_config(self) -> None:
        """
        Initialize Streamlit page configuration.
        
        Follows constitutional principles by using clear, documented configuration.
        """
        st.set_page_config(
            page_title='GDP Dashboard - Cerebrum-1',
            page_icon=':earth_americas:',
            layout='wide',  # Efficiency optimization (CHRONOS)
            initial_sidebar_state='expanded'
        )
    
    def render_header(self) -> None:
        """
        Render the application header with constitution compliance info.
        
        Provides clarity about the application's governance (Article 4).
        """
        st.title(':earth_americas: GDP Dashboard')
        
        # Constitutional compliance indicator
        with st.expander("🏛️ Constitutional Compliance", expanded=False):
            st.markdown("""
            **Repository Constitution: cerebrum-1**
            
            - ✅ **AEGIS** (Security): Environment-based configuration
            - ✅ **PORTABILITÉ** (Portability): Open standards, cross-platform
            - ✅ **HYGIE** (Resilience): Comprehensive testing and validation
            - ✅ **CHRONOS** (Efficiency): Optimized data processing and caching
            
            *This application follows the constitutional principles defined in `/docs/CONSTITUTION.md`*
            """)
        
        st.markdown("""
        Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. 
        As you'll notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
        But it's otherwise a great (and did I mention _free_?) source of data.
        """)
        
        st.divider()
    
    def render_controls(self) -> Tuple[List[str], int, int]:
        """
        Render user input controls for data filtering.
        
        Returns:
            Tuple of (selected_countries, year_from, year_to)
        """
        try:
            # Get data for controls
            min_year, max_year = self.data_processor.get_year_range()
            available_countries = self.data_processor.get_available_countries()
            
            # Year range slider with validation (HYGIE)
            st.subheader("📅 Time Period Selection")
            year_from, year_to = st.slider(
                'Which years are you interested in?',
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year),
                help="Select the time period for GDP analysis"
            )
            
            # Country selection with default values
            st.subheader("🌍 Country Selection")
            default_countries = ['USA', 'CHN', 'DEU', 'FRA', 'GBR', 'JPN']
            # Filter defaults to only include available countries
            valid_defaults = [c for c in default_countries if c in available_countries]
            
            selected_countries = st.multiselect(
                'Which countries would you like to view?',
                available_countries,
                default=valid_defaults[:6],  # Limit to first 6 for performance (CHRONOS)
                help="Select countries to compare GDP data"
            )
            
            # Validation warning (HYGIE)
            if not selected_countries:
                st.warning("⚠️ Please select at least one country to display data.")
            
            return selected_countries, year_from, year_to
            
        except Exception as e:
            logger.error(f"Error rendering controls: {e}")
            st.error(f"Failed to load control data: {e}")
            return [], 0, 0
    
    def render_line_chart(self, filtered_data: pd.DataFrame) -> None:
        """
        Render GDP trend line chart.
        
        Args:
            filtered_data: Filtered GDP data to display
        """
        if filtered_data.empty:
            st.warning("📊 No data available for the selected criteria.")
            return
        
        st.subheader("📈 GDP Trends Over Time")
        
        # Performance optimization: ensure data is properly typed (CHRONOS)
        chart_data = filtered_data.copy()
        chart_data['Year'] = pd.to_numeric(chart_data['Year'], errors='coerce')
        chart_data['GDP'] = pd.to_numeric(chart_data['GDP'], errors='coerce')
        
        # Remove any invalid data points for chart stability (HYGIE)
        chart_data = chart_data.dropna(subset=['Year', 'GDP'])
        
        if chart_data.empty:
            st.warning("📊 No valid data points after filtering.")
            return
        
        try:
            st.line_chart(
                chart_data,
                x='Year',
                y='GDP',
                color='Country Code',
                use_container_width=True
            )
            
            # Data quality information
            with st.expander("📊 Data Quality Information"):
                st.metric("Total Data Points", len(chart_data))
                countries_with_data = chart_data['Country Code'].nunique()
                st.metric("Countries with Data", countries_with_data)
                
        except Exception as e:
            logger.error(f"Error rendering line chart: {e}")
            st.error("Failed to render chart. Please check your data selection.")
    
    def render_metrics_grid(self, filtered_data: pd.DataFrame, 
                          year_from: int, year_to: int, 
                          selected_countries: List[str]) -> None:
        """
        Render GDP metrics in a grid layout.
        
        Args:
            filtered_data: Filtered GDP data
            year_from: Start year for comparison
            year_to: End year for comparison
            selected_countries: List of selected countries
        """
        if filtered_data.empty or not selected_countries:
            return
        
        st.subheader(f"💰 GDP Metrics for {year_to}")
        
        # Get comparison data for growth calculations
        try:
            first_year_data = filtered_data[filtered_data['Year'] == year_from]
            last_year_data = filtered_data[filtered_data['Year'] == year_to]
            
            # Create columns for metrics display (responsive layout)
            num_countries = len(selected_countries)
            if num_countries <= 3:
                cols = st.columns(num_countries)
            else:
                cols = st.columns(4)  # Maximum 4 columns for readability (CHRONOS)
            
            for i, country in enumerate(selected_countries):
                col = cols[i % len(cols)]
                
                with col:
                    self._render_country_metric(
                        country, first_year_data, last_year_data,
                        year_from, year_to
                    )
                    
        except Exception as e:
            logger.error(f"Error rendering metrics grid: {e}")
            st.error("Failed to calculate metrics. Please verify your data selection.")
    
    def _render_country_metric(self, country: str, 
                              first_year_data: pd.DataFrame,
                              last_year_data: pd.DataFrame,
                              year_from: int, year_to: int) -> None:
        """
        Render metric for a single country.
        
        Args:
            country: Country code
            first_year_data: GDP data for start year
            last_year_data: GDP data for end year
            year_from: Start year
            year_to: End year
        """
        try:
            # Extract GDP values with error handling (HYGIE)
            first_gdp_row = first_year_data[first_year_data['Country Code'] == country]
            last_gdp_row = last_year_data[last_year_data['Country Code'] == country]
            
            # Handle missing data gracefully
            if first_gdp_row.empty or last_gdp_row.empty:
                st.metric(
                    label=f'{country} GDP',
                    value='N/A',
                    delta='No data available',
                    delta_color='off'
                )
                return
            
            first_gdp = first_gdp_row['GDP'].iloc[0]
            last_gdp = last_gdp_row['GDP'].iloc[0]
            
            # Calculate growth and format values
            growth_text, delta_color = self.metrics_calculator.calculate_growth_metric(
                first_gdp, last_gdp
            )
            
            formatted_gdp = self.metrics_calculator.format_gdp_billions(last_gdp)
            
            st.metric(
                label=f'{country} GDP ({year_to})',
                value=formatted_gdp,
                delta=f'{growth_text} since {year_from}' if growth_text != 'n/a' else 'Growth: N/A',
                delta_color=delta_color
            )
            
        except Exception as e:
            logger.error(f"Error rendering metric for {country}: {e}")
            st.metric(
                label=f'{country} GDP',
                value='Error',
                delta='Calculation failed',
                delta_color='off'
            )
    
    def render_footer(self) -> None:
        """
        Render application footer with governance information.
        """
        st.divider()
        
        with st.container():
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**🏛️ Governance**")
                st.markdown("Repository: cerebrum-1")
                st.markdown("Constitution: `/docs/CONSTITUTION.md`")
            
            with col2:
                st.markdown("**🔒 Security (AEGIS)**")
                st.markdown("✅ Environment-based config")
                st.markdown("✅ No hardcoded secrets")
            
            with col3:
                st.markdown("**📊 Data Source**")
                st.markdown("[World Bank Open Data](https://data.worldbank.org/)")
                st.markdown("Updated: 2022")
    
    def run(self) -> None:
        """
        Main application entry point.
        
        Orchestrates the entire dashboard rendering process.
        """
        try:
            # Render UI components in order
            self.render_header()
            
            # Get user inputs
            selected_countries, year_from, year_to = self.render_controls()
            
            # Process and display data if countries are selected
            if selected_countries:
                # Filter data based on selections
                filtered_data = self.data_processor.filter_data(
                    selected_countries, year_from, year_to
                )
                
                # Render visualizations
                self.render_line_chart(filtered_data)
                st.divider()
                self.render_metrics_grid(
                    filtered_data, year_from, year_to, selected_countries
                )
            
            # Always render footer
            self.render_footer()
            
        except Exception as e:
            logger.error(f"Critical error in dashboard: {e}")
            st.error("🚨 Application encountered a critical error. Please refresh the page.")
            
            # Show error details in debug mode
            if st.checkbox("Show Debug Information"):
                st.exception(e)
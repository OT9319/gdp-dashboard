# GDP Dashboard Documentation

## Overview

The GDP Dashboard is a Streamlit-based web application for visualizing GDP data from the World Bank Open Data. This application is built following the constitutional requirements for security, portability, resilience, and efficiency.

## Constitution Compliance

This application strictly adheres to the Constitution du Repository "cerebrum-1":

### Article 1: JUNCTURE (Role and Purpose)
- Serves as the definitive source for GDP data visualization
- Maintains coherence through structured architecture
- Ensures quality through comprehensive testing and documentation

### Article 2: Inviolable Guiding Principles

#### Clause 2.1 - AEGIS (Security)
- **Environment Variables**: All configuration is loaded from environment variables
- **No Hardcoded Secrets**: Zero hardcoded sensitive information
- **Secure Defaults**: Safe default values for all configurations
- **Input Validation**: Comprehensive validation of user inputs and data

#### Clause 2.2 - PORTABILITÉ (Portability)
- **Open Standards**: Built with Python, Streamlit, and standard CSV format
- **Cross-Platform**: Works on any system supporting Python 3.8+
- **Standard Libraries**: Uses only well-established open-source libraries
- **Data Format Independence**: Easily adaptable to different data sources

#### Clause 2.3 - HYGIE (Resilience)
- **Comprehensive Testing**: Full test suite covering all functionality
- **Error Handling**: Graceful degradation and informative error messages
- **Data Validation**: Robust validation of data integrity
- **Fallback Mechanisms**: Safe defaults when data is missing or invalid

#### Clause 2.4 - CHRONOS (Efficiency)
- **Smart Caching**: Configurable TTL-based caching of data
- **Optimized Processing**: Efficient pandas operations
- **Performance Monitoring**: Logging and metrics for performance tracking
- **Lazy Loading**: Data loaded only when needed

### Article 3: Operational Workflow
- **AI Copilot Integration**: Ready for AI-assisted development and review
- **Human Barrier Respect**: Final deployment decisions reserved for human oversight
- **Code Review Ready**: Structured for comprehensive review processes

### Article 4: Execution Directives
- **Clarity**: Comprehensive docstrings and comments throughout
- **Documentation**: This documentation and inline API docs
- **Structure**: Proper separation into `/src`, `/docs`, `/tests`, `/prompts`

## Architecture

```
gdp-dashboard/
├── src/                    # Source code
│   └── gdp_dashboard.py   # Main application module
├── docs/                   # Documentation
│   └── README.md          # This file
├── tests/                  # Test suite
│   └── test_gdp_dashboard.py
├── prompts/               # AI prompts and templates
├── data/                  # Data files
│   └── gdp_data.csv      # World Bank GDP data
├── streamlit_app.py       # Main entry point
├── requirements.txt       # Dependencies
└── CONSTITUTION.md        # Constitutional framework
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration
Create a `.env` file or set environment variables:

```bash
# Optional: Custom data path
GDP_DATA_PATH=data/gdp_data.csv

# Optional: Cache TTL in seconds (default: 3600)
CACHE_TTL_SECONDS=3600

# Optional: Year range (defaults: 1960-2022)
MIN_YEAR=1960
MAX_YEAR=2022
```

### Running the Application
```bash
streamlit run streamlit_app.py
```

## Features

### Core Functionality
- **Interactive Year Selection**: Slider to select time ranges
- **Country Comparison**: Multi-select dropdown for country selection
- **Time Series Visualization**: Line chart showing GDP trends over time
- **Metrics Dashboard**: Key GDP metrics with growth calculations
- **Responsive Layout**: Adapts to different screen sizes

### Advanced Features
- **Smart Caching**: Automatic caching with configurable TTL
- **Error Recovery**: Graceful handling of missing or invalid data
- **Performance Monitoring**: Logging for debugging and optimization
- **Security**: No hardcoded secrets, environment-based configuration
- **Accessibility**: Clear labeling and help text for all controls

## Data Source

The application uses GDP data from the [World Bank Open Data](https://data.worldbank.org/) initiative. The data includes:

- **Coverage**: 1960-2022 (may vary by country)
- **Format**: CSV with country codes and yearly GDP values
- **Currency**: USD (current prices)
- **Update Frequency**: Annual

### Data Structure
```csv
Country Code,1960,1961,1962,...,2022
USA,543300000000,563300000000,...,25462700000000
GBR,72330000000,76780000000,...,3131378000000
```

## API Reference

### Core Functions

#### `get_gdp_data() -> pd.DataFrame`
Loads and processes GDP data with caching.

**Returns:**
- `pd.DataFrame`: Processed data with columns ['Country Code', 'Year', 'GDP']

**Raises:**
- `FileNotFoundError`: If data file is missing
- `pd.errors.EmptyDataError`: If data file is empty
- `ValueError`: If data format is invalid

#### `get_config_value(key: str, default: str) -> str`
Securely retrieves configuration from environment variables.

**Parameters:**
- `key`: Environment variable name
- `default`: Default value if env var not set

**Returns:**
- `str`: Configuration value

#### `validate_country_selection(countries: List[str], selected: List[str]) -> List[str]`
Validates and filters country selections.

**Parameters:**
- `countries`: Available country codes
- `selected`: User-selected country codes

**Returns:**
- `List[str]`: Validated country codes

#### `calculate_gdp_metrics(gdp_df: pd.DataFrame, country: str, from_year: int, to_year: int) -> Tuple[float, float, str, str]`
Calculates GDP metrics for visualization.

**Parameters:**
- `gdp_df`: GDP DataFrame
- `country`: Country code
- `from_year`: Starting year
- `to_year`: Ending year

**Returns:**
- `Tuple`: (first_gdp_billions, last_gdp_billions, growth_text, delta_color)

## Testing

The application includes comprehensive tests following the HYGIE principle:

### Running Tests
```bash
cd tests
python -m pytest test_gdp_dashboard.py -v
```

### Test Coverage
- **Security Tests**: Validates no hardcoded secrets
- **Data Processing Tests**: Validates data loading and transformation
- **Error Handling Tests**: Validates graceful error handling
- **Performance Tests**: Validates caching and optimization
- **Constitutional Compliance Tests**: Validates adherence to constitution

### Test Categories
1. **Configuration Security**: Environment variable handling
2. **Data Processing**: Core data manipulation functions
3. **Data Integrity**: Validation of data quality
4. **Error Handling**: Edge cases and error scenarios
5. **Performance**: Caching and optimization
6. **Constitutional Compliance**: Meta-tests for constitution adherence

## Performance Optimization

### Caching Strategy
- **Data Caching**: GDP data cached with configurable TTL
- **Smart Invalidation**: Cache refreshes when data changes
- **Memory Efficient**: Minimal memory footprint

### Performance Monitoring
```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"Loaded GDP data: {len(gdp_df)} records")
```

### Optimization Tips
- Set appropriate `CACHE_TTL_SECONDS` for your use case
- Monitor logs for performance insights
- Use efficient country selections for large datasets

## Security Considerations

### Data Protection
- No sensitive data stored in the application
- All data is public World Bank information
- No user authentication required

### Configuration Security
- All configuration via environment variables
- No hardcoded secrets or credentials
- Safe defaults for all settings

### Input Validation
- All user inputs validated and sanitized
- SQL injection not applicable (no database)
- XSS protection via Streamlit's built-in escaping

## Troubleshooting

### Common Issues

#### "GDP data file not found"
**Solution:** Ensure `data/gdp_data.csv` exists or set `GDP_DATA_PATH` environment variable.

#### "Application startup error"
**Solution:** Check Python version (3.8+ required) and install all dependencies.

#### "No data available for selected countries"
**Solution:** Try different country codes or year ranges.

### Debugging
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help
1. Check application logs for detailed error messages
2. Verify environment configuration
3. Run test suite to identify issues
4. Review constitution compliance

## Contributing

### Code Standards
- Follow constitutional requirements
- Add tests for new functionality
- Include comprehensive docstrings
- Use type hints where appropriate
- Follow PEP 8 style guidelines

### Pull Request Process
1. Ensure constitutional compliance
2. Add/update tests
3. Update documentation
4. Request human barrier review (per Article 3)

## License

This project follows the repository's LICENSE file and constitutional framework.

## Changelog

### Version 1.0.0 (Constitution Implementation)
- ✅ Constitutional compliance implementation
- ✅ Modular architecture (/src, /docs, /tests, /prompts)
- ✅ Comprehensive security (AEGIS)
- ✅ Open standards compliance (PORTABILITÉ)
- ✅ Full test coverage (HYGIE)
- ✅ Performance optimizations (CHRONOS)
- ✅ Enhanced documentation and API reference
- ✅ Error handling and data validation
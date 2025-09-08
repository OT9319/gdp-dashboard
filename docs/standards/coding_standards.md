# Coding Standards - GDP Dashboard

## AEGIS (Security) Standards

### 1. Secrets Management
- ❌ **Never commit secrets to version control**
- ✅ Use environment variables for sensitive data
- ✅ Use `.env` files with proper `.gitignore` patterns
- ✅ Store secrets in secure vaults (GitHub Secrets, AWS Secrets Manager)

```python
# ❌ Bad
API_KEY = "sk-1234567890abcdef"

# ✅ Good
import os
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")
```

### 2. Input Validation
- ✅ Always validate user inputs
- ✅ Use type hints for better code safety
- ✅ Sanitize data before processing

```python
def process_user_input(data: str) -> str:
    """Process user input with proper validation."""
    if not isinstance(data, str):
        raise TypeError("Input must be a string")
    
    if len(data.strip()) == 0:
        raise ValueError("Input cannot be empty")
    
    # Sanitize and process data
    return data.strip().lower()
```

### 3. Error Handling
- ✅ Use specific exception types
- ✅ Log security-relevant events
- ✅ Don't expose sensitive information in error messages

```python
try:
    result = process_sensitive_data(user_input)
except ValidationError as e:
    logger.warning(f"Invalid input attempt: {type(e).__name__}")
    raise ValueError("Invalid input provided") from None  # Don't expose details
```

## PORTABILITÉ (Portability) Standards

### 1. Cross-Platform Compatibility
- ✅ Use `pathlib.Path` for file paths
- ✅ Avoid platform-specific code
- ✅ Use standard library when possible

```python
from pathlib import Path

# ✅ Good - works on all platforms
data_path = Path(__file__).parent / "data" / "file.csv"

# ❌ Bad - Unix-specific
data_path = os.path.join(os.path.dirname(__file__), "data/file.csv")
```

### 2. Dependency Management
- ✅ Pin dependency versions in requirements.txt
- ✅ Use well-maintained, popular libraries
- ✅ Avoid deprecated packages

```txt
# requirements.txt
streamlit==1.49.1
pandas>=2.0.0,<3.0.0
numpy>=1.21.0
```

### 3. Configuration Management
- ✅ Use configuration files
- ✅ Support environment-based configuration
- ✅ Provide sensible defaults

```python
import os
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration."""
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    data_path: str = os.getenv("DATA_PATH", "data/gdp_data.csv")
    cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))
```

## HYGIE (Testing) Standards

### 1. Test Structure
- ✅ Follow the Arrange-Act-Assert pattern
- ✅ One assertion per test when possible
- ✅ Use descriptive test names

```python
def test_get_gdp_data_returns_dataframe_with_correct_columns():
    """Test that get_gdp_data returns a DataFrame with expected columns."""
    # Arrange
    expected_columns = ['Country Code', 'Year', 'GDP']
    
    # Act
    result = get_gdp_data()
    
    # Assert
    assert isinstance(result, pd.DataFrame)
    for col in expected_columns:
        assert col in result.columns
```

### 2. Test Coverage
- ✅ Aim for 80%+ test coverage
- ✅ Test edge cases and error conditions
- ✅ Mock external dependencies

```python
@patch('streamlit_app.pd.read_csv')
def test_get_gdp_data_handles_missing_file(mock_read_csv):
    """Test that get_gdp_data handles missing data file gracefully."""
    # Arrange
    mock_read_csv.side_effect = FileNotFoundError("File not found")
    
    # Act & Assert
    with pytest.raises(FileNotFoundError):
        get_gdp_data()
```

### 3. Test Organization
- ✅ Separate unit and integration tests
- ✅ Use fixtures for common test data
- ✅ Clean up after tests

```python
# tests/conftest.py
@pytest.fixture
def sample_gdp_data():
    """Provide sample GDP data for testing."""
    return pd.DataFrame({
        'Country Code': ['USA', 'FRA'],
        '2020': [21000000, 2600000],
        '2021': [22000000, 2700000]
    })
```

## CHRONOS (Performance) Standards

### 1. Algorithm Efficiency
- ✅ Choose appropriate data structures
- ✅ Understand time complexity
- ✅ Optimize hot paths

```python
# ✅ Good - O(1) lookup
country_lookup = {code: name for code, name in country_pairs}
result = country_lookup.get(search_code)

# ❌ Bad - O(n) search
for code, name in country_pairs:
    if code == search_code:
        result = name
        break
```

### 2. Memory Management
- ✅ Use generators for large datasets
- ✅ Clean up resources explicitly
- ✅ Monitor memory usage

```python
def process_large_dataset(file_path: Path) -> Iterator[dict]:
    """Process large dataset without loading everything into memory."""
    with open(file_path, 'r') as f:
        for line in f:
            yield process_line(line)  # Generator - memory efficient
```

### 3. Caching
- ✅ Cache expensive computations
- ✅ Use appropriate cache strategies
- ✅ Set cache expiration policies

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_gdp_data() -> pd.DataFrame:
    """Load and process GDP data with caching."""
    # Expensive operation
    return processed_data
```

## Code Style Standards

### 1. Naming Conventions
- ✅ Use descriptive names
- ✅ Follow PEP 8 conventions
- ✅ Use constants for magic numbers

```python
# ✅ Good
MIN_YEAR = 1960
MAX_YEAR = 2022
GDP_BILLION_DIVISOR = 1_000_000_000

def calculate_gdp_growth_rate(initial_gdp: float, final_gdp: float) -> float:
    """Calculate GDP growth rate between two periods."""
    return (final_gdp - initial_gdp) / initial_gdp * 100
```

### 2. Function Design
- ✅ Single responsibility principle
- ✅ Keep functions small (< 50 lines)
- ✅ Use type hints

```python
def filter_data_by_year_range(
    df: pd.DataFrame, 
    start_year: int, 
    end_year: int
) -> pd.DataFrame:
    """Filter DataFrame to include only specified year range."""
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
```

### 3. Error Messages
- ✅ Provide helpful error messages
- ✅ Include context when possible
- ✅ Suggest solutions

```python
if not data_file.exists():
    raise FileNotFoundError(
        f"GDP data file not found: {data_file}. "
        f"Please ensure the file exists or check the DATA_PATH configuration."
    )
```

## Documentation Standards

### 1. Code Comments
- ✅ Explain why, not what
- ✅ Reference the relevant principle (AEGIS, CHRONOS, etc.)
- ✅ Keep comments up to date

```python
# CHRONOS: Use vectorized operations for better performance with large datasets
gdp_billions = df['GDP'] / GDP_BILLION_DIVISOR

# AEGIS: Validate country codes to prevent injection attacks
if not re.match(r'^[A-Z]{3}$', country_code):
    raise ValueError(f"Invalid country code format: {country_code}")
```

### 2. Docstrings
- ✅ Use Google-style docstrings
- ✅ Include examples when helpful
- ✅ Document all parameters and return values

### 3. README and Documentation
- ✅ Keep documentation current
- ✅ Include setup and usage instructions
- ✅ Provide examples

## Git and Version Control

### 1. Commit Messages
- ✅ Use conventional commit format
- ✅ Reference the relevant principle
- ✅ Be descriptive but concise

```
feat(AEGIS): add secret scanning to CI pipeline

- Implement automated secret detection
- Add security checks for API keys and passwords
- Configure fail-fast for detected secrets
```

### 2. Branch Strategy
- ✅ Use feature branches
- ✅ Keep branches up to date
- ✅ Use pull requests for code review

### 3. .gitignore
- ✅ Ignore secrets and credentials
- ✅ Ignore build artifacts
- ✅ Include environment-specific files

```gitignore
# AEGIS: Security - never commit secrets
.env
*.key
secrets/
config/production.yml

# Build artifacts
__pycache__/
*.pyc
dist/
build/
```

---

*These standards ensure code quality, security, and maintainability while following the AEGIS-PORTABILITÉ-HYGIE-CHRONOS principles.*
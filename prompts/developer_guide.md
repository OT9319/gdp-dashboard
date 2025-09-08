# Developer Guidelines for Constitutional Compliance

## Overview
This guide helps developers contribute to the cerebrum-1 repository while adhering to constitutional principles.

## Before You Start

### 1. Understand the Constitution
Read `/docs/CONSTITUTION.md` thoroughly before making any changes.

### 2. Review the Workflow  
Familiarize yourself with `/docs/WORKFLOW.md` for the contribution process.

### 3. Set Up Your Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Set up data path (AEGIS compliance)
export GDP_DATA_PATH=/path/to/your/data/gdp_data.csv

# Run tests to ensure everything works
python tests/run_tests.py
```

## Constitutional Checklist

### 🛡️ AEGIS (Security) - MANDATORY
Before committing, ensure:
- [ ] No hardcoded API keys, passwords, or secrets
- [ ] Use environment variables for configuration
- [ ] No sensitive data in logs or error messages
- [ ] Proper input validation and sanitization

**Example - Good:**
```python
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API_KEY environment variable required")
```

**Example - Bad:**
```python
api_key = "sk-1234567890abcdef"  # CONSTITUTIONAL VIOLATION!
```

### 🌐 PORTABILITÉ (Portability) - MANDATORY
- [ ] Use cross-platform file paths (pathlib.Path)
- [ ] Avoid platform-specific dependencies
- [ ] Use open standards and formats
- [ ] Framework-agnostic design where possible

**Example - Good:**
```python
from pathlib import Path
data_path = Path(__file__).parent / 'data' / 'file.csv'
```

**Example - Bad:**
```python
data_path = "C:\\Windows\\data\\file.csv"  # Platform-specific!
```

### 🏥 HYGIE (Resilience) - MANDATORY
- [ ] Write tests for all new functionality
- [ ] Implement comprehensive error handling
- [ ] Validate all inputs and edge cases
- [ ] Use type hints for better code safety

**Example - Good:**
```python
def process_data(values: List[float]) -> float:
    """Process values with error handling."""
    if not values:
        raise ValueError("Cannot process empty value list")
    
    try:
        return sum(values) / len(values)
    except (TypeError, ZeroDivisionError) as e:
        logger.error(f"Data processing failed: {e}")
        raise
```

### ⏱️ CHRONOS (Efficiency) - MANDATORY
- [ ] Optimize algorithm complexity where possible
- [ ] Use appropriate data structures
- [ ] Implement caching for expensive operations  
- [ ] Profile performance-critical code

**Example - Good:**
```python
@st.cache_data
def expensive_calculation(data: pd.DataFrame) -> pd.DataFrame:
    """Cached expensive operation."""
    return data.groupby('category').agg({'value': 'sum'})
```

## File Organization (Article 4)

### Directory Structure
```
/src/           # Main source code
/docs/          # Documentation
/tests/         # Unit and integration tests
/prompts/       # AI agent prompts and guides
/data/          # Data files (if any)
```

### Naming Conventions
- Files: `snake_case.py`
- Classes: `PascalCase` 
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

## Documentation Standards

### Module Docstrings (Required)
```python
"""
Module Description

This module implements [functionality] following constitutional principles:
- Security (AEGIS): [how security is addressed]
- Portability (PORTABILITÉ): [how portability is ensured]  
- Resilience (HYGIE): [how resilience is implemented]
- Efficiency (CHRONOS): [how efficiency is optimized]
"""
```

### Function Docstrings (Required for Public Functions)
```python
def process_gdp_data(data: pd.DataFrame, 
                    countries: List[str]) -> pd.DataFrame:
    """
    Process GDP data for specified countries.
    
    Args:
        data: Raw GDP DataFrame
        countries: List of country codes to include
        
    Returns:
        Filtered and processed DataFrame
        
    Raises:
        ValueError: If data is invalid or empty
        TypeError: If countries parameter is not a list
    """
```

## Testing Requirements

### Unit Tests (Mandatory)
- Test all public methods
- Test error conditions
- Test edge cases and boundary values
- Aim for >80% test coverage

### Integration Tests (Recommended)
- Test component interactions
- Test end-to-end workflows
- Test configuration scenarios

### Running Tests
```bash
# Run all constitutional tests
python tests/run_tests.py

# Run specific test file
python -m unittest tests.test_gdp_core

# Run with coverage (if installed)
coverage run -m unittest discover tests/
coverage report
```

## Commit Message Format

```
type(scope): description

Examples:
feat(core): add GDP filtering with environment config (AEGIS)
fix(ui): resolve cross-platform path issue (PORTABILITÉ)
test(integration): add resilience tests for data processing (HYGIE)
perf(core): optimize data caching for better performance (CHRONOS)
docs(constitution): update security guidelines
security(core): remove hardcoded API key vulnerability
```

## Pull Request Template

```markdown
## Constitutional Compliance Checklist

### 🛡️ AEGIS (Security)
- [ ] No secrets or sensitive data exposed
- [ ] Environment variables used for configuration
- [ ] Input validation implemented

### 🌐 PORTABILITÉ (Portability)
- [ ] Cross-platform compatibility verified
- [ ] Open standards used
- [ ] No vendor lock-in introduced

### 🏥 HYGIE (Resilience)  
- [ ] Tests written for new functionality
- [ ] Error handling implemented
- [ ] Edge cases covered

### ⏱️ CHRONOS (Efficiency)
- [ ] Performance considerations addressed
- [ ] Efficient algorithms used
- [ ] Resource usage optimized

## Changes Description
[Describe your changes and how they comply with constitutional principles]

## Testing
[Describe how you tested your changes]

## Risk Assessment
- Risk Level: LOW/MEDIUM/HIGH
- Breaking Changes: YES/NO
- Performance Impact: POSITIVE/NEUTRAL/NEGATIVE
```

## Common Mistakes to Avoid

1. **Hardcoding secrets** - Always use environment variables
2. **Platform-specific paths** - Use pathlib.Path
3. **Missing error handling** - Always handle potential failures
4. **No tests** - Every new feature needs tests
5. **Poor performance** - Profile and optimize critical paths
6. **Missing documentation** - Document all public interfaces

## Getting Help

- Read the constitution: `/docs/CONSTITUTION.md`
- Check workflow guide: `/docs/WORKFLOW.md`  
- Run tests: `python tests/run_tests.py`
- Ask questions in pull request comments

Remember: The Human Barrier makes final decisions, but following these guidelines will make the review process smoother and ensure constitutional compliance.
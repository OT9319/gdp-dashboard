# Documentation Templates and Standards

## Python Docstring Template

```python
def function_name(param1: type, param2: type = default) -> return_type:
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the purpose, algorithm,
    or important implementation details.
    
    Args:
        param1 (type): Description of the first parameter.
        param2 (type, optional): Description of the second parameter. 
            Defaults to default.
    
    Returns:
        return_type: Description of what is returned.
    
    Raises:
        ValueError: If param1 is invalid.
        TypeError: If param2 is not the expected type.
    
    Example:
        >>> result = function_name("hello", 42)
        >>> print(result)
        "Expected output"
    
    Note:
        Any important notes about usage, performance considerations,
        or compatibility issues.
    
    See Also:
        related_function: Description of how it relates.
        https://docs.python.org/3/: Link to relevant external docs.
    """
    pass
```

## Class Docstring Template

```python
class ClassName:
    """
    Brief description of the class purpose.
    
    Detailed explanation of what the class represents, its main
    responsibilities, and how it fits into the larger system.
    
    Attributes:
        attr1 (type): Description of the first attribute.
        attr2 (type): Description of the second attribute.
    
    Example:
        >>> instance = ClassName(param="value")
        >>> result = instance.method()
        >>> print(result)
    
    Note:
        Important information about class usage, threading safety,
        or performance characteristics.
    """
    
    def __init__(self, param: type):
        """
        Initialize the class instance.
        
        Args:
            param (type): Description of initialization parameter.
        """
        pass
    
    def method_name(self, arg: type) -> type:
        """
        Brief description of the method.
        
        Args:
            arg (type): Description of the argument.
        
        Returns:
            type: Description of return value.
        """
        pass
```

## Module Docstring Template

```python
"""
Module Name: Brief description of the module.

This module provides functionality for [main purpose]. It includes
classes and functions for [key capabilities].

Classes:
    ClassName: Brief description of what it does.
    
Functions:
    function_name: Brief description of what it does.

Constants:
    CONSTANT_NAME: Description of the constant.

Example:
    Basic usage of the module:
    
    >>> import module_name
    >>> result = module_name.function_name()
    
Author:
    Your Name (your.email@domain.com)
    
Created:
    YYYY-MM-DD
    
Version:
    1.0.0
"""
```

## API Documentation Template

```python
def api_endpoint(request_data: dict) -> dict:
    """
    Brief description of the API endpoint.
    
    This endpoint handles [specific functionality] and returns
    [type of response].
    
    Args:
        request_data (dict): The incoming request data containing:
            - field1 (str): Description of required field.
            - field2 (int, optional): Description of optional field.
    
    Returns:
        dict: Response data containing:
            - status (str): Success/error status.
            - data (list): List of result objects.
            - message (str): Human-readable message.
    
    Raises:
        ValidationError: If request_data is malformed.
        AuthenticationError: If authentication fails.
        RateLimitError: If rate limit is exceeded.
    
    HTTP Status Codes:
        200: Success
        400: Bad Request - Invalid input data
        401: Unauthorized - Authentication failed
        429: Too Many Requests - Rate limit exceeded
        500: Internal Server Error
    
    Example:
        >>> request = {"field1": "value", "field2": 123}
        >>> response = api_endpoint(request)
        >>> print(response["status"])
        "success"
    
    See Also:
        related_endpoint: Description of related functionality.
    """
    pass
```

## README Template

```markdown
# Project Name

Brief description of what the project does and its main purpose.

## 🚀 Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## 📋 Requirements

- Python 3.8+
- Required packages (see requirements.txt)
- Other system requirements

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/repository.git
   cd repository
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 💻 Usage

### Basic Usage
```python
from project import main_function

result = main_function(param="value")
print(result)
```

### Advanced Usage
```python
from project import AdvancedClass

instance = AdvancedClass()
result = instance.advanced_method()
```

## 📚 Documentation

- [API Documentation](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Development Guide](docs/development.md)

## 🧪 Testing

Run tests using:
```bash
python -m unittest discover tests/
```

## 📊 Performance

- Metric 1: Performance information
- Metric 2: Benchmarks or limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see LICENSE file.

## 👥 Authors

- Author Name - Initial work - [@username](https://github.com/username)

## 🙏 Acknowledgments

- Inspiration or libraries used
- Contributors
- Special thanks
```

## Code Comments Guidelines

### Good Comments:
```python
# AEGIS: Validate input to prevent security issues
if not isinstance(api_key, str) or len(api_key) < 16:
    raise ValueError("API key must be at least 16 characters")

# CHRONOS: Use binary search for O(log n) performance
left, right = 0, len(sorted_list) - 1
while left <= right:
    mid = (left + right) // 2
    # ... binary search logic

# PORTABILITÉ: Support both Unix and Windows paths
path = Path(file_path).resolve()  # Cross-platform path handling
```

### Comments to Avoid:
```python
# Bad: Obvious comments
x = x + 1  # Increment x

# Bad: Outdated comments
# TODO: Fix this bug (fixed 3 months ago)

# Bad: Commented-out code
# old_function(param)  # Remove this line entirely
```
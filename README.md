# 🌍 GDP Dashboard - With IA Agent Integration

A Streamlit-based dashboard for exploring GDP data from the World Bank, enhanced with an **Integration Manifest for IA Agent** following the cerebrum-1 principles.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gdp-dashboard-template.streamlit.app/)
![AEGIS Security](https://img.shields.io/badge/Security-AEGIS-red)
![HYGIE Tests](https://img.shields.io/badge/Tests-HYGIE-green)
![CHRONOS Performance](https://img.shields.io/badge/Performance-CHRONOS-blue)
![PORTABILITÉ Standards](https://img.shields.io/badge/Standards-PORTABILIT%C3%89-orange)

## 🛡️ Integration Manifest

This repository implements an **Integration Manifest for IA Agent** following the constitutional principles:

- **🛡️ AEGIS (Security)**: Automated secret scanning and dependency security checks
- **🌐 PORTABILITÉ (Portability)**: Cross-platform compatibility and standard libraries
- **🧪 HYGIE (Testing)**: Comprehensive test suite with unit and integration tests
- **⚡ CHRONOS (Performance)**: Optimized algorithms and performance monitoring

The IA Agent serves as the **Guardian of the "Book of Origins"**, maintaining code quality, security, and consistency.

## 🚀 Features

- 📊 Interactive GDP data visualization
- 🔍 Multi-country comparison with time series charts
- 📈 Growth rate calculations and metrics
- 🛡️ Built-in security scanning (AEGIS)
- 🧪 Comprehensive testing framework (HYGIE)
- ⚡ Performance-optimized data processing (CHRONOS)
- 🌐 Cross-platform compatibility (PORTABILITÉ)

## 📋 Requirements

- Python 3.8+
- Streamlit 1.49+
- Pandas 2.0+
- See `requirements.txt` for complete dependencies

## 🛠️ Installation

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/OT9319/gdp-dashboard.git
   cd gdp-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run streamlit_app.py
   ```

### Development Setup

1. **Install additional development dependencies:**
   ```bash
   pip install pytest pytest-cov black flake8 mypy
   ```

2. **Run the security scan:**
   ```bash
   python scripts/security/scan-secrets.py
   ```

3. **Run the test suite:**
   ```bash
   python -m unittest discover tests/
   ```

## 💻 Usage

### Basic Usage

The dashboard provides an interactive interface to:
- Select year ranges using the slider
- Choose countries using the multi-select dropdown  
- View GDP trends in the line chart
- Compare growth metrics in the summary cards

### Advanced Usage

#### Data Loading Function
```python
from streamlit_app import get_gdp_data

# Load and process GDP data
df = get_gdp_data()
print(f"Loaded {len(df)} rows of GDP data")
```

#### Security Scanning
```bash
# Scan for secrets in the repository
python scripts/security/scan-secrets.py --path . --output json

# Check dependencies for vulnerabilities  
python scripts/security/check-dependencies.py --requirements requirements.txt
```

#### Running Tests
```bash
# Unit tests
python -m unittest discover tests/unit/

# Integration tests  
python -m unittest discover tests/integration/

# All tests with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

## 🏗️ Project Structure

```
gdp-dashboard/
├── 📁 src/                    # Source code (future modules)
├── 📁 prompts/               # IA Agent templates and prompts
│   ├── doc-templates/        # Documentation templates
│   └── test-templates/       # Test templates
├── 📁 docs/                  # Project documentation
│   ├── INTEGRATION_MANIFEST.md
│   └── standards/            # Coding standards
├── 📁 tests/                 # Test suites
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── 📁 scripts/               # Utility scripts
│   └── security/             # AEGIS security tools
├── 📁 data/                  # GDP data files
├── 📁 .github/              # GitHub workflows
│   └── workflows/            # CI/CD pipelines
├── 📄 streamlit_app.py       # Main application
└── 📄 requirements.txt       # Dependencies
```

## 🧪 Testing (HYGIE)

### Test Coverage
- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test system integration and real data processing
- **Security Tests**: Validate AEGIS security measures

### Running Tests
```bash
# Run all tests
python -m unittest discover tests/ -v

# Run specific test categories
python -m unittest tests.unit.test_streamlit_app
python -m unittest tests.integration.test_gdp_dashboard

# Generate coverage report
python -m pytest tests/ --cov=. --cov-report=html
```

## 🛡️ Security (AEGIS)

### Automated Security Scanning

The repository includes automated security scanning tools:

```bash
# Scan for secrets and credentials
python scripts/security/scan-secrets.py

# Check dependencies for known vulnerabilities
python scripts/security/check-dependencies.py
```

### Security Features
- 🔍 Secret detection in code and commits
- 📦 Dependency vulnerability scanning
- 🚫 No hardcoded credentials or API keys
- ✅ Environment variable configuration
- 🔒 Secure handling of sensitive data

## ⚡ Performance (CHRONOS)

### Optimizations
- **Data Caching**: Streamlit cache for expensive data operations
- **Efficient Processing**: Pandas vectorized operations
- **Memory Management**: Optimized data structures
- **Lazy Loading**: Data loaded only when needed

### Performance Monitoring
```bash
# Check application performance
python -c "
import time
from streamlit_app import get_gdp_data
start = time.time()
df = get_gdp_data()
print(f'Load time: {time.time() - start:.2f}s')
print(f'Memory usage: ~{df.memory_usage(deep=True).sum() / 1024 / 1024:.1f}MB')
"
```

## 🌐 Portability (PORTABILITÉ)

### Cross-Platform Support
- ✅ Works on Windows, macOS, and Linux
- ✅ Uses pathlib for cross-platform paths
- ✅ Standard library dependencies when possible
- ✅ Environment-based configuration

### Standards Compliance
- 📝 PEP 8 code style
- 🔍 Type hints for better code clarity
- 📚 Comprehensive docstrings
- 🧪 Test-driven development

## 🤖 IA Agent Integration

The repository follows an **Integration Manifest** that guides the IA Agent as the "Guardian of the Book of Origins":

### Agent Responsibilities
1. **Code Review**: Automated quality and security checks
2. **Testing**: Ensure comprehensive test coverage
3. **Documentation**: Maintain up-to-date documentation
4. **Performance**: Monitor and optimize application performance
5. **Security**: Continuous security scanning and best practices

### Workflow Integration
- 🔄 **Pull Request Checks**: Automated AEGIS security scans
- 🧪 **Test Automation**: HYGIE test execution on commits
- 📊 **Performance Monitoring**: CHRONOS performance baseline checks
- 📋 **Standards Compliance**: PORTABILITÉ coding standards validation

## 🔧 Development

### Code Standards
Follow the [Coding Standards](docs/standards/coding_standards.md) document for:
- Security best practices (AEGIS)
- Testing guidelines (HYGIE)  
- Performance optimization (CHRONOS)
- Portability requirements (PORTABILITÉ)

### Documentation Standards
Use the templates in `prompts/doc-templates/` for:
- Function docstrings
- Class documentation
- API documentation
- Code comments

## 📊 CI/CD Pipeline

The repository includes automated GitHub Actions workflows:
- **Security Scanning**: AEGIS secret and dependency checks
- **Code Quality**: Linting, formatting, and type checking
- **Testing**: HYGIE unit and integration test execution
- **Performance**: CHRONOS performance baseline validation
- **Compliance**: Integration manifest compliance checking

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch following the manifest principles
3. **Implement** changes with appropriate tests and documentation
4. **Run** security scans and tests locally
5. **Submit** a pull request

All contributions are automatically validated against the Integration Manifest.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **OT9319** - Repository maintainer
- **IA Agent** - Guardian of code quality and security (Integration Manifest)

## 🙏 Acknowledgments

- **World Bank Open Data** - GDP data source
- **Streamlit** - Web application framework
- **cerebrum-1 principles** - Integration manifest inspiration

---

*This repository demonstrates the implementation of an IA Agent Integration Manifest following AEGIS-PORTABILITÉ-HYGIE-CHRONOS principles for maintainable, secure, and high-quality code.*

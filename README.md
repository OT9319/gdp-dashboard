# 🌍 GDP Dashboard - Constitution Compliant

A comprehensive Streamlit application for visualizing GDP data from the World Bank Open Data, built according to the **Constitution du Repository "cerebrum-1"**.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gdp-dashboard-template.streamlit.app/)

## 🏛️ Constitutional Compliance

This application strictly adheres to all constitutional requirements:

- **🔒 AEGIS (Security)**: Environment-based configuration, no hardcoded secrets
- **🔄 PORTABILITÉ (Portability)**: Open standards (Python, Streamlit, CSV)
- **🛡️ HYGIE (Resilience)**: Comprehensive test coverage and error handling
- **⚡ CHRONOS (Efficiency)**: Optimized data processing with intelligent caching

## 📁 Architecture

```
gdp-dashboard/
├── src/                    # Source code (Article 4)
├── docs/                   # Comprehensive documentation
├── tests/                  # Full test suite (HYGIE)
├── prompts/               # AI copilot templates (Article 3)
├── data/                  # World Bank GDP data
├── CONSTITUTION.md        # Fundamental law
└── streamlit_app.py       # Application entry point
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gdp-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (Optional)
   ```bash
   cp .env.template .env
   # Edit .env with your preferences
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Run tests** (HYGIE Compliance)
   ```bash
   python tests/test_gdp_dashboard.py
   ```

## 🎯 Features

### Core Features
- 📊 Interactive GDP data visualization
- 🌐 Multi-country comparison
- 📈 Time series analysis with customizable ranges
- 💰 GDP metrics with growth calculations
- 📱 Responsive design for all devices

### Constitutional Features
- 🔐 **Security First**: All configuration via environment variables
- 🧪 **Test Coverage**: Comprehensive test suite for reliability
- 📚 **Documentation**: Extensive documentation and inline comments
- ⚡ **Performance**: Smart caching and optimized data processing
- 🔄 **Portability**: Built with open standards and durable technologies

## 📖 Documentation

- **[Complete Documentation](docs/README.md)**: Comprehensive guide and API reference
- **[Constitution](CONSTITUTION.md)**: Repository fundamental law
- **[AI Prompts](prompts/)**: Copilot assistance templates

## 🧪 Testing (HYGIE Compliance)

Run the comprehensive test suite:

```bash
# Run all tests
python tests/test_gdp_dashboard.py

# Test constitutional compliance
python -c "from tests.test_gdp_dashboard import TestConstitutionalCompliance; import unittest; unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestConstitutionalCompliance))"
```

## ⚙️ Configuration (AEGIS Compliance)

All configuration is managed through environment variables for security:

| Variable | Default | Description |
|----------|---------|-------------|
| `GDP_DATA_PATH` | `data/gdp_data.csv` | Path to GDP data file |
| `CACHE_TTL_SECONDS` | `3600` | Data cache duration |
| `MIN_YEAR` | `1960` | Minimum year for data |
| `MAX_YEAR` | `2022` | Maximum year for data |

## 🤖 AI Copilot Integration (Article 3)

This repository includes structured prompts for AI assistance:
- Code review templates
- Security analysis workflows  
- Performance optimization guidance
- Documentation enhancement tools

**Note**: Final merge decisions remain with the Human Barrier per constitutional Article 3.

## 🔧 Development

### Code Standards
- Follow constitutional requirements (all 4 articles)
- Add tests for new functionality (HYGIE)
- Include comprehensive docstrings (Article 4)
- Use environment variables for configuration (AEGIS)

### Pull Request Process
1. Ensure constitutional compliance
2. Add/update tests
3. Update documentation  
4. Request human barrier review

## 📊 Data Source

GDP data from [World Bank Open Data](https://data.worldbank.org/):
- **Coverage**: 266 countries, 1960-2022
- **Format**: CSV with yearly GDP values
- **Currency**: USD (current prices)
- **License**: CC BY 4.0

## 📜 License

This project follows the repository's LICENSE file and constitutional framework.

---

*Built with ❤️ following the Constitution du Repository "cerebrum-1"*

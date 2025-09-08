# :earth_americas: GDP Dashboard - Constitutional Implementation

A GDP Dashboard application restructured according to the **Constitution du Repository "cerebrum-1"** principles.

[![Constitutional Compliance](https://img.shields.io/badge/Constitutional-Compliant-green.svg)]()
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gdp-dashboard-template.streamlit.app/)

## 🏛️ Constitutional Governance

This repository operates under the **Constitution du Repository "cerebrum-1"**, implementing four core principles:

- **🛡️ AEGIS (Security)**: Environment-based configuration, no hardcoded secrets
- **🌐 PORTABILITÉ (Portability)**: Cross-platform design with open standards
- **🏥 HYGIE (Resilience)**: Comprehensive testing and error handling
- **⏱️ CHRONOS (Efficiency)**: Optimized data processing and caching

## 📁 Repository Structure

```
├── src/                    # Main source code (constitutional)
│   ├── gdp_core.py        # Core data processing logic
│   ├── gdp_ui.py          # User interface components
│   └── main.py            # Application entry point
├── docs/                   # Documentation
│   ├── CONSTITUTION.md    # Repository constitution
│   └── WORKFLOW.md        # Pull request workflow
├── tests/                  # Test suite
│   ├── test_gdp_core.py   # Core functionality tests
│   ├── test_integration.py # Integration tests
│   └── run_tests.py       # Constitutional test runner
├── prompts/               # AI agent prompts
│   ├── code_review_agent.md # Code review guidelines
│   └── developer_guide.md   # Developer instructions
├── data/                  # GDP data files
└── streamlit_app.py       # Legacy compatibility entry point
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/OT9319/gdp-dashboard.git
   cd gdp-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment (optional)**
   ```bash
   export GDP_DATA_PATH=/path/to/your/gdp_data.csv
   ```

### Running the Application

#### Option 1: Constitutional Entry Point (Recommended)
```bash
streamlit run src/main.py
```

#### Option 2: Legacy Compatibility
```bash
streamlit run streamlit_app.py
```

### Validating Constitutional Compliance

```bash
# Run full constitutional test suite
python tests/run_tests.py

# Run specific test categories
python -m unittest tests.test_gdp_core
python -m unittest tests.test_integration
```

## 🔧 Development

### For Contributors

1. **Read the Constitution**: `/docs/CONSTITUTION.md`
2. **Follow the Workflow**: `/docs/WORKFLOW.md`
3. **Use Developer Guide**: `/prompts/developer_guide.md`

### Development Workflow

```bash
# 1. Validate current state
python tests/run_tests.py

# 2. Make your changes following constitutional principles

# 3. Run tests to ensure compliance
python tests/run_tests.py

# 4. Submit pull request for Human Barrier review
```

### Constitutional Checklist

Before submitting code, ensure:
- [ ] **AEGIS**: No hardcoded secrets, environment variables used
- [ ] **PORTABILITÉ**: Cross-platform compatibility
- [ ] **HYGIE**: Tests written for new functionality
- [ ] **CHRONOS**: Performance considerations addressed

## 🏗️ Architecture

### Core Components

- **`GDPDataProcessor`**: Handles data loading, processing, and caching
- **`GDPMetricsCalculator`**: Calculates GDP metrics and growth indicators
- **`GDPDashboardUI`**: Manages Streamlit user interface components

### Security Features

- Environment variable configuration
- Sensitive data detection
- Secure default settings
- Input validation and sanitization

### Performance Optimizations

- Streamlit caching for data processing
- Efficient pandas operations
- Responsive UI design
- Memory-conscious data handling

## 📊 Data Source

GDP data sourced from [World Bank Open Data](https://data.worldbank.org/) (updated through 2022).

## 🤖 AI Agent Integration

This repository includes AI agent prompts for:
- **Code Review**: Automated constitutional compliance checking
- **Development**: Guided development following constitutional principles

See `/prompts/` directory for detailed agent instructions.

## 📝 Constitutional Documents

- [`/docs/CONSTITUTION.md`](docs/CONSTITUTION.md) - Repository governing principles
- [`/docs/WORKFLOW.md`](docs/WORKFLOW.md) - Pull request and governance workflow
- [`/prompts/developer_guide.md`](prompts/developer_guide.md) - Developer instructions

## 🧪 Testing

The repository includes comprehensive tests validating all constitutional principles:

```bash
# Full constitutional compliance validation
python tests/run_tests.py

# Expected output:
# ✅ Repository is fully compliant with cerebrum-1 constitution
# ✅ All principles validated:
#    🛡️  AEGIS (Security): Environment-based config, no secrets
#    🌐 PORTABILITÉ (Portability): Cross-platform, open standards
#    🏥 HYGIE (Resilience): Comprehensive testing, error handling
#    ⏱️  CHRONOS (Efficiency): Optimized processing, caching
```

## 🚨 Governance

This repository operates under constitutional governance:
- **AI Agent**: Provides automated code review and analysis
- **Human Barrier**: Makes final merge decisions
- **Constitutional Compliance**: All code must adhere to four core principles

## 📄 License

[View License](LICENSE)

---

*This repository demonstrates the implementation of constitutional governance principles in software development, serving as both a functional GDP dashboard and a reference implementation for structured repository governance.*

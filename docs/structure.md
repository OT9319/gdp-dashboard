# Project Directory Structure

This document describes the organization of the GDP Dashboard project repository.

## Directory Layout

```
gdp-dashboard/
├── src/                    # Main source code
│   └── streamlit_app.py   # Primary Streamlit application
├── data/                   # Data files
│   └── gdp_data.csv       # GDP dataset from World Bank
├── docs/                   # Documentation
│   └── structure.md       # This file - project structure documentation
├── tests/                  # Unit and integration tests
├── prompts/               # AI prompts and instructions
├── .github/               # GitHub configuration (workflows, etc.)
├── .devcontainer/         # Development container configuration
├── requirements.txt       # Python dependencies
├── README.md             # Project overview and setup instructions
└── LICENSE               # Project license
```

## Directory Descriptions

### `/src`
Contains the main source code of the application. All Python modules and primary application logic should be placed here.

- **streamlit_app.py**: The main Streamlit application that provides an interactive GDP data visualization dashboard.

### `/data`
Contains data files used by the application.

- **gdp_data.csv**: GDP data sourced from the World Bank Open Data, containing historical GDP figures by country from 1960 to 2022.

### `/docs`
Documentation for the project, including setup instructions, API documentation, and architectural decisions.

- **structure.md**: This file documenting the project organization.

### `/tests`
Unit tests, integration tests, and test utilities. All test files should follow the naming convention `test_*.py` or `*_test.py`.

### `/prompts`
AI prompts, instructions, and related materials for AI-assisted development and documentation generation.

### `.github`
GitHub-specific configuration files including:
- Workflows for CI/CD
- Issue templates
- Pull request templates
- Code owners configuration

### `.devcontainer`
Development container configuration for consistent development environments across different machines.

## Contributing Guidelines

When contributing to this project:

1. **Source Code**: Place all new Python modules in the `/src` directory
2. **Tests**: Add corresponding tests in the `/tests` directory
3. **Documentation**: Update relevant documentation in `/docs` when adding new features
4. **Data**: Place any new data files in the `/data` directory
5. **AI Materials**: Store prompts and AI-related instructions in `/prompts`

## Running the Application

To run the application with the new structure:

```bash
# From the project root directory
streamlit run src/streamlit_app.py
```

## Path References

When referencing files from within the source code, use relative paths from the project root:
- Data files: `../data/filename.csv` (from `/src`)
- Documentation: `../docs/filename.md` (from `/src`)
- Tests: `../tests/test_filename.py` (from `/src`)
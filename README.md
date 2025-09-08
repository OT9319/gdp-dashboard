# :earth_americas: GDP Dashboard with Constitutional Architecture API

A Streamlit app showing GDP data combined with a FastAPI backend that provides Zapier integration endpoints for the Constitutional Architecture system (CEREBRUM-1).

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gdp-dashboard-template.streamlit.app/)

## Features

- **📊 GDP Dashboard**: Interactive visualization of world GDP data
- **🔗 Constitutional Architecture API**: FastAPI backend with Zapier integration endpoints
- **🛡️ AEGIS Security**: Content filtering system for constitutional compliance
- **⚡ Task Management**: API endpoints for task creation and workload reporting

## Quick Start

### Option 1: Start Everything (Recommended)
```bash
./start.sh
```
This starts both the Streamlit dashboard and the API endpoints.

### Option 2: Run Components Separately

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the GDP Dashboard**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Run the API (in another terminal)**
   ```bash
   python -m api.main
   ```

## API Endpoints

The Constitutional Architecture API provides endpoints for Zapier integration:

- `GET /` - Health check
- `POST /api/auth/token` - Get JWT authentication token
- `POST /api/security/filter` - AEGIS content filtering
- `POST /api/tasks` - Create new tasks
- `GET /api/tasks/workload` - Get workload summary
- `GET /api/tasks` - List all tasks

### Testing the API

Run the comprehensive test suite:
```bash
python test_api.py
```

## Zapier Integration

This system implements the three key Zapier integrations for the Constitutional Architecture:

1. **Zap #1**: Triage Constitutionnel de l'Inbox (Notion → API → Notion)
2. **Zap #2**: Weekly Workload Report (Schedule → API → Email)
3. **Zap #3**: Email to Notion Inbox (Gmail → Notion)

See [ZAPIER_INTEGRATION.md](ZAPIER_INTEGRATION.md) for detailed configuration instructions.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │     Zapier      │
│  GDP Dashboard  │    │  Constitution   │    │  Integrations   │
│   (Port 8501)   │    │   API (8000)    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   CEREBRUM-1    │
                    │ Constitutional  │
                    │ Architecture    │
                    └─────────────────┘
```

## Environment Variables

Set these in production:

```bash
export JWT_SECRET_KEY="your-super-secure-secret-key"
```

## Development

The project structure:
```
├── streamlit_app.py          # Original GDP dashboard
├── api/
│   ├── __init__.py
│   └── main.py              # FastAPI application
├── data/
│   └── gdp_data.csv         # GDP dataset
├── requirements.txt         # Python dependencies
├── start.sh                # Startup script
├── test_api.py             # API test suite
└── ZAPIER_INTEGRATION.md   # Detailed Zapier setup guide
```

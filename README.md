# 🏛️ GDP Dashboard with Constitutional APIs

A comprehensive system featuring both a Streamlit GDP dashboard and a constitutional APIs backend built with FastAPI.

## 🚀 Features

### 📊 GDP Dashboard (Streamlit)
- Interactive GDP data visualization
- Country comparison and filtering
- Time-series analysis
- Data from World Bank Open Data

### 🏛️ Constitutional APIs (FastAPI)
- **Constitutional Architecture** - Validation and compliance built into the system structure
- **JWT Authentication** - Secure authentication with role-based access control
- **Task Management** - Full CRUD operations with constitutional validation
- **Audit Logging** - Comprehensive audit trail with constitutional compliance scoring
- **PostgreSQL Integration** - Robust database with SQLAlchemy ORM
- **Docker Ready** - Multi-service deployment configuration

## 🏗️ Architecture

The system implements **Constitutional Architecture** principles:

- ⚖️ **Validation by Design** - All inputs validated with Pydantic schemas
- 🔐 **Security First** - JWT tokens with constitutional claims
- 📊 **Compliance Scoring** - Automatic constitutional compliance scoring
- 🔒 **Access Control** - Role-based permissions
- 📝 **Audit Trail** - Comprehensive logging with constitutional compliance
- 🗂️ **Data Integrity** - UUID-based identification and versioning

## 🚀 Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd gdp-dashboard
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the applications:
- **Constitutional APIs**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Streamlit Dashboard**: http://localhost:8501

### Manual Installation

#### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Poetry (optional) or pip

#### Install Dependencies

With Poetry:
```bash
poetry install
```

With pip:
```bash
pip install -r requirements.txt
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-jose passlib bcrypt pytest pytest-asyncio httpx asyncpg email-validator python-multipart
```

#### Set Environment Variables
```bash
export DATABASE_URL=postgresql://gdp_user:gdp_password@localhost:5432/gdp_dashboard
export JWT_SECRET_KEY=your-secret-key-change-in-production
export ENVIRONMENT=development
```

#### Run the Applications

**Constitutional APIs (FastAPI):**
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Streamlit Dashboard:**
```bash
streamlit run streamlit_app.py
```

## 📋 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - User logout

### Task Management
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/` - List tasks with filtering
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `POST /api/tasks/{id}/complete` - Mark task as complete

### System
- `GET /health` - Health check with constitutional status
- `GET /info` - System information
- `GET /docs` - Interactive API documentation

## 🔐 Authentication

The system uses JWT tokens with constitutional claims:

1. **Register a user:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
    "role": "user"
  }'
```

2. **Login to get token:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=SecurePass123!"
```

3. **Use token in requests:**
```bash
curl -X GET "http://localhost:8000/api/tasks/" \
  -H "Authorization: Bearer <your-jwt-token>"
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests  
pytest tests/integration/ -v

# All tests with coverage
pytest tests/ --cov=src --cov-report=html
```

## 🏛️ Constitutional Principles

The system embodies constitutional architecture principles:

### 1. **Validation by Design**
All input validation is built into Pydantic schemas with constitutional rules:
```python
class TaskCreate(ConstitutionalBaseSchema):
    title: str = Field(..., min_length=1, max_length=200)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    
    @field_validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
```

### 2. **Constitutional Compliance Scoring**
Every entity automatically calculates its constitutional compliance:
```python
def calculate_compliance_score(self) -> int:
    score = 0
    if self.title and len(self.title.strip()) > 0:
        score += 10
    if self.description:
        score += 10
    return min(score, 100)
```

### 3. **Audit Trail**
All operations are logged with constitutional principles:
```python
await log_audit_event(
    db=db,
    action="CREATE",
    entity_type="Task", 
    entity_id=task.id,
    constitutional_score=task.compliance_score
)
```

## 📁 Project Structure

```
gdp-dashboard/
├── 🏛️ Constitutional APIs
│   ├── src/
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database configuration
│   │   ├── auth.py              # Authentication system
│   │   ├── models/
│   │   │   ├── db_models.py     # SQLAlchemy models
│   │   │   └── schemas.py       # Pydantic schemas
│   │   ├── routes/
│   │   │   ├── auth.py          # Authentication routes
│   │   │   └── tasks.py         # Task management routes
│   │   └── middleware/
│   │       └── audit.py         # Audit logging
│   ├── tests/
│   │   ├── unit/                # Unit tests
│   │   ├── integration/         # Integration tests
│   │   └── conftest.py          # Test configuration
│   ├── Dockerfile               # API container
│   ├── docker-compose.yml       # Multi-service setup
│   └── pyproject.toml           # Project configuration
├── 📊 Streamlit Dashboard
│   ├── streamlit_app.py         # Dashboard application
│   ├── data/
│   │   └── gdp_data.csv         # GDP dataset
│   ├── Dockerfile.streamlit     # Dashboard container
│   └── requirements.txt         # Python dependencies
└── 📄 Documentation
    ├── README.md                # This file
    └── scripts/
        └── init-db.sql          # Database initialization
```

## 🐳 Docker Services

The `docker-compose.yml` defines:

- **PostgreSQL Database** (Port 5432)
- **Redis Cache** (Port 6379) 
- **Constitutional APIs** (Port 8000)
- **Streamlit Dashboard** (Port 8501)

All services include health checks and proper networking.

## 🛠️ Development

### Database Migrations

The system uses SQLAlchemy with constitutional base models. Tables are created automatically in development, but use Alembic for production migrations.

### Adding New Features

1. Create constitutional models in `src/models/db_models.py`
2. Add Pydantic schemas in `src/models/schemas.py` 
3. Implement routes with constitutional validation
4. Add comprehensive tests
5. Update audit logging if needed

### Constitutional Validation Rules

Add validation rules by extending the constitutional base classes:

```python
class MyConstitutionalModel(ConstitutionalBase):
    # Your fields here
    
    def calculate_compliance_score(self) -> int:
        # Custom compliance logic
        return score
```

## 📜 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow constitutional architecture principles
4. Add comprehensive tests
5. Submit a pull request

## 🆘 Support

- 📚 **API Documentation**: http://localhost:8000/docs
- 🏥 **Health Check**: http://localhost:8000/health
- 📊 **System Info**: http://localhost:8000/info

---

Built with ❤️ using Constitutional Architecture principles

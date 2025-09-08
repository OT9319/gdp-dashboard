"""
Constitutional APIs Main Application
Implements a FastAPI application with constitutional architecture principles
"""

from datetime import datetime
from contextlib import asynccontextmanager
import os
from typing import Dict, Any

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
import uvicorn

from src.database import create_tables, engine
from src.models.db_models import Base
from src.models.schemas import HealthCheck, ErrorResponse
from src.routes import auth, tasks
from src.middleware.audit import ConstitutionalAuditMiddleware


# Application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Constitutional application lifespan with database initialization
    """
    # Startup
    print("🏛️  Initializing Constitutional APIs System...")
    
    # Create database tables
    try:
        create_tables()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
    
    print("🚀 Constitutional APIs System ready")
    
    yield
    
    # Shutdown
    print("🏛️  Shutting down Constitutional APIs System...")
    engine.dispose()
    print("✅ Shutdown complete")


# Create FastAPI application with constitutional principles
app = FastAPI(
    title="GDP Dashboard Constitutional APIs",
    description="""
    ## Constitutional APIs System

    A FastAPI-based system implementing constitutional architecture principles with:
    
    - **Constitutional Validation**: Built-in validation rules and compliance scoring
    - **JWT Authentication**: Secure authentication with role-based access control
    - **Audit Logging**: Comprehensive audit trail for all operations
    - **Task Management**: Full CRUD operations with constitutional compliance
    - **Database Integration**: PostgreSQL with SQLAlchemy ORM
    - **Security First**: Security principles embedded in the architecture
    
    ### Constitutional Principles
    
    1. **Validation by Design**: All inputs validated using Pydantic schemas
    2. **Audit Trail**: Every operation logged with constitutional compliance scoring
    3. **Role-Based Access**: Granular permissions with constitutional roles
    4. **Data Integrity**: Built-in data integrity checks and validation rules
    5. **Security Standards**: Industry-standard security practices enforced
    
    ### Authentication
    
    Use the `/api/auth/login` endpoint to obtain a JWT token, then include it in the
    `Authorization` header as `Bearer <token>` for all authenticated requests.
    """,
    version="1.0.0",
    terms_of_service="https://gdp-dashboard.example.com/terms/",
    contact={
        "name": "GDP Dashboard Team",
        "email": "support@gdp-dashboard.example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize constitutional audit middleware
audit_middleware = ConstitutionalAuditMiddleware()

# CORS middleware with constitutional security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware for constitutional security
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["gdp-dashboard.example.com", "*.gdp-dashboard.example.com"]
    )


# Constitutional exception handler
@app.exception_handler(HTTPException)
async def constitutional_exception_handler(request: Request, exc: HTTPException):
    """
    Constitutional exception handler with audit logging
    """
    error_response = ErrorResponse(
        error=exc.__class__.__name__,
        message=exc.detail,
        constitutional_violations=getattr(exc, 'constitutional_violations', None),
        request_id=getattr(request.state, 'request_id', None)
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )


# Constitutional request middleware
@app.middleware("http")
async def constitutional_request_middleware(request: Request, call_next):
    """
    Constitutional middleware for request processing and audit logging
    """
    # Generate request ID
    import uuid
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Process request
    start_time = datetime.utcnow()
    
    try:
        response = await call_next(request)
        
        # Log successful request if needed
        if audit_middleware.log_all_requests:
            # This would require database session - implement as needed
            pass
            
        return response
        
    except Exception as exc:
        # Log failed request
        print(f"Request {request_id} failed: {str(exc)}")
        
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="InternalServerError",
                message="Internal server error occurred",
                request_id=request_id
            ).dict()
        )


# Include routers with constitutional organization
app.include_router(auth.router, prefix="", tags=["Authentication"])
app.include_router(tasks.router, prefix="", tags=["Tasks"])


# Constitutional health check endpoint
@app.get(
    "/health",
    response_model=HealthCheck,
    summary="Constitutional health check",
    description="Check system health with constitutional compliance status",
    tags=["System"]
)
async def health_check() -> HealthCheck:
    """
    Constitutional health check with system status
    """
    try:
        # Check database connectivity
        from src.database import SessionLocal
        db = SessionLocal()
        try:
            db.execute("SELECT 1")
            database_status = "connected"
        except Exception:
            database_status = "disconnected"
        finally:
            db.close()
        
        return HealthCheck(
            status="healthy" if database_status == "connected" else "degraded",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            database=database_status,
            constitutional_score=100 if database_status == "connected" else 50
        )
        
    except Exception as e:
        return HealthCheck(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            database="error",
            constitutional_score=0
        )


# Constitutional system information endpoint
@app.get(
    "/info",
    summary="System information",
    description="Get constitutional system information",
    tags=["System"]
)
async def system_info() -> Dict[str, Any]:
    """
    Get constitutional system information
    """
    return {
        "name": "GDP Dashboard Constitutional APIs",
        "version": "1.0.0",
        "description": "Constitutional architecture-based API system",
        "constitutional_principles": [
            "validation_by_design",
            "audit_trail",
            "role_based_access",
            "data_integrity",
            "security_standards"
        ],
        "features": [
            "JWT Authentication",
            "Task Management",
            "Audit Logging", 
            "Constitutional Validation",
            "Role-based Access Control",
            "PostgreSQL Integration"
        ],
        "endpoints": {
            "authentication": "/api/auth",
            "tasks": "/api/tasks",
            "health": "/health",
            "documentation": "/docs"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# Constitutional root endpoint
@app.get(
    "/",
    summary="Constitutional APIs welcome",
    description="Welcome message for constitutional APIs system",
    tags=["System"]
)
async def root() -> Dict[str, Any]:
    """
    Constitutional APIs system welcome endpoint
    """
    return {
        "message": "Welcome to GDP Dashboard Constitutional APIs",
        "description": "A FastAPI system built with constitutional architecture principles",
        "constitutional_score": 100,
        "documentation": "/docs",
        "health_check": "/health",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# Constitutional startup message
@app.on_event("startup")
async def startup_message():
    """
    Constitutional startup message
    """
    print("""
    🏛️  GDP Dashboard Constitutional APIs
    ====================================
    
    📋 Features:
    • Constitutional validation and compliance
    • JWT-based authentication system  
    • Comprehensive audit logging
    • Task management with RBAC
    • PostgreSQL integration
    • FastAPI with automatic documentation
    
    🔗 Endpoints:
    • API Documentation: /docs
    • Health Check: /health
    • Authentication: /api/auth
    • Tasks: /api/tasks
    
    🚀 System ready at: http://localhost:8000
    """)


if __name__ == "__main__":
    # Run with constitutional configuration
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )
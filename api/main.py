"""
FastAPI application for Zapier integration endpoints
Supports the Constitutional Architecture system described in the briefing
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import jwt
import os
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Constitutional Architecture API",
    description="API endpoints for Zapier integration with AEGIS security system",
    version="1.0.0"
)

# CORS middleware for web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security setup
security = HTTPBearer()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"

# Data Models
class FilterRequest(BaseModel):
    content: str

class FilterResponse(BaseModel):
    is_compliant: bool
    reason: Optional[str] = None
    confidence: float = 1.0

class TaskCreate(BaseModel):
    name: str
    priority: str = "💡 Normal"
    content: Optional[str] = None
    source: Optional[str] = "zapier"

class Task(BaseModel):
    id: str
    name: str
    priority: str
    content: Optional[str] = None
    status: str = "pending"
    created_at: datetime
    estimated_minutes: int = 15

class WorkloadSummary(BaseModel):
    total_minutes: int
    tasks_by_priority: Dict[str, int]
    total_tasks: int
    status_breakdown: Dict[str, int]

# In-memory storage (in production, use a proper database)
tasks_storage: List[Task] = []

# Authentication functions
def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token for AEGIS authentication"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT token for authentication"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

# AEGIS Content Filtering
def aegis_content_filter(content: str) -> FilterResponse:
    """
    AEGIS Constitutional compliance filter
    This is a simplified implementation - in production, this would use
    more sophisticated content analysis
    """
    # Basic compliance rules
    forbidden_patterns = [
        "urgent", "asap", "emergency", "crisis",  # Anti-rush patterns
        "hack", "bypass", "override",  # Security concerns
    ]
    
    content_lower = content.lower()
    
    # Check for forbidden patterns
    for pattern in forbidden_patterns:
        if pattern in content_lower:
            return FilterResponse(
                is_compliant=False,
                reason=f"Content contains forbidden pattern: '{pattern}'",
                confidence=0.9
            )
    
    # Check minimum content quality
    if len(content.strip()) < 10:
        return FilterResponse(
            is_compliant=False,
            reason="Content too short for proper assessment",
            confidence=0.8
        )
    
    # Default: compliant
    return FilterResponse(
        is_compliant=True,
        confidence=0.95
    )

# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Constitutional Architecture API is running",
        "system": "CEREBRUM-1",
        "aegis_status": "active"
    }

@app.post("/api/security/filter", response_model=FilterResponse)
async def filter_content(
    request: FilterRequest,
    current_user: dict = Depends(verify_jwt_token)
):
    """
    AEGIS content filtering endpoint for Zapier Zap #1
    Filters content for constitutional compliance
    """
    logger.info(f"Filtering content for user: {current_user.get('sub', 'unknown')}")
    
    try:
        result = aegis_content_filter(request.content)
        logger.info(f"Filter result: {result.is_compliant}")
        return result
    except Exception as e:
        logger.error(f"Error filtering content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing content filter"
        )

@app.post("/api/tasks", response_model=Task)
async def create_task(
    task_request: TaskCreate,
    current_user: dict = Depends(verify_jwt_token)
):
    """
    Create new task endpoint for Zapier Zap #1
    Creates tasks after AEGIS filtering
    """
    logger.info(f"Creating task for user: {current_user.get('sub', 'unknown')}")
    
    try:
        # Generate task ID
        task_id = f"task_{len(tasks_storage) + 1}_{int(datetime.now().timestamp())}"
        
        # Estimate minutes based on priority
        priority_minutes = {
            "🔥 Urgent": 30,
            "⚡ High": 20,
            "💡 Normal": 15,
            "📝 Low": 10
        }
        
        estimated_minutes = priority_minutes.get(task_request.priority, 15)
        
        # Create task
        new_task = Task(
            id=task_id,
            name=task_request.name,
            priority=task_request.priority,
            content=task_request.content,
            created_at=datetime.now(),
            estimated_minutes=estimated_minutes
        )
        
        # Store task
        tasks_storage.append(new_task)
        
        logger.info(f"Created task: {task_id}")
        return new_task
        
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating task"
        )

@app.get("/api/tasks/workload", response_model=WorkloadSummary)
async def get_workload_summary(
    current_user: dict = Depends(verify_jwt_token)
):
    """
    Get workload summary for Zapier Zap #2
    Returns weekly workload report
    """
    logger.info(f"Getting workload for user: {current_user.get('sub', 'unknown')}")
    
    try:
        # Calculate totals
        total_minutes = sum(task.estimated_minutes for task in tasks_storage)
        total_tasks = len(tasks_storage)
        
        # Group by priority
        priority_counts = {}
        for task in tasks_storage:
            priority_counts[task.priority] = priority_counts.get(task.priority, 0) + task.estimated_minutes
        
        # Group by status
        status_counts = {}
        for task in tasks_storage:
            status_counts[task.status] = status_counts.get(task.status, 0) + 1
        
        workload = WorkloadSummary(
            total_minutes=total_minutes,
            tasks_by_priority=priority_counts,
            total_tasks=total_tasks,
            status_breakdown=status_counts
        )
        
        logger.info(f"Workload summary: {total_tasks} tasks, {total_minutes} minutes")
        return workload
        
    except Exception as e:
        logger.error(f"Error getting workload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving workload data"
        )

@app.get("/api/tasks", response_model=List[Task])
async def get_tasks(
    current_user: dict = Depends(verify_jwt_token),
    limit: int = 100
):
    """Get all tasks (for debugging and monitoring)"""
    return tasks_storage[:limit]

@app.post("/api/auth/token")
async def create_access_token(username: str = "zapier", system: str = "CEREBRUM-1"):
    """
    Create JWT access token for testing
    In production, this should be properly secured with credentials
    """
    access_token = create_jwt_token(
        data={"sub": username, "system": system}
    )
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
Pydantic schemas for Constitutional APIs
Implements constitutional validation principles with comprehensive input/output validation
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from enum import Enum

from src.models.db_models import TaskStatus, TaskPriority, UserRole


# Constitutional base schemas with validation
class ConstitutionalBaseSchema(BaseModel):
    """Base schema with constitutional validation principles"""
    
    class Config:
        # Enable ORM mode for SQLAlchemy compatibility
        from_attributes = True
        # Validate assignment to prevent corruption
        validate_assignment = True
        # Use enum values instead of names
        use_enum_values = True
        # JSON encoders for custom types
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }


# User schemas
class UserBase(ConstitutionalBaseSchema):
    """Base user schema with constitutional validation"""
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=100, description="Unique username")
    full_name: Optional[str] = Field(None, max_length=200, description="User's full name")
    role: UserRole = Field(default=UserRole.USER, description="User's role in the system")
    
    @validator('username')
    def validate_username(cls, v):
        """Constitutional username validation"""
        if not v.isalnum() and '_' not in v and '-' not in v:
            raise ValueError('Username must contain only alphanumeric characters, underscores, or hyphens')
        return v.lower()
    
    @validator('full_name')
    def validate_full_name(cls, v):
        """Constitutional full name validation"""
        if v and len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters long')
        return v.strip() if v else v


class UserCreate(UserBase):
    """Schema for creating new users"""
    password: str = Field(..., min_length=8, description="User's password")
    confirm_password: str = Field(..., description="Password confirmation")
    
    @validator('password')
    def validate_password(cls, v):
        """Constitutional password validation"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @root_validator
    def validate_passwords_match(cls, values):
        """Ensure passwords match"""
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValueError('Passwords do not match')
        return values


class UserUpdate(ConstitutionalBaseSchema):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=200)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user responses"""
    id: UUID
    is_verified: bool
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class UserLogin(ConstitutionalBaseSchema):
    """Schema for user login"""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User's password")


# Task schemas
class TaskBase(ConstitutionalBaseSchema):
    """Base task schema with constitutional validation"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=5000, description="Task description")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    tags: Optional[List[str]] = Field(default_factory=list, description="Task tags")
    metadata_json: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('title')
    def validate_title(cls, v):
        """Constitutional title validation"""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        """Constitutional description validation"""
        return v.strip() if v else v
    
    @validator('tags')
    def validate_tags(cls, v):
        """Constitutional tags validation"""
        if v is None:
            return []
        # Remove duplicates and validate each tag
        validated_tags = []
        for tag in v:
            tag = tag.strip().lower()
            if tag and len(tag) <= 50 and tag.isalnum():
                validated_tags.append(tag)
        return list(set(validated_tags))
    
    @validator('due_date')
    def validate_due_date(cls, v):
        """Constitutional due date validation"""
        if v and v <= datetime.now():
            raise ValueError('Due date must be in the future')
        return v


class TaskCreate(TaskBase):
    """Schema for creating new tasks"""
    assigned_to: Optional[UUID] = Field(None, description="User ID to assign the task to")
    validation_rules: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Constitutional validation rules")


class TaskUpdate(ConstitutionalBaseSchema):
    """Schema for updating tasks"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[UUID] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    metadata_json: Optional[Dict[str, Any]] = None
    validation_rules: Optional[Dict[str, Any]] = None


class TaskResponse(TaskBase):
    """Schema for task responses"""
    id: UUID
    status: TaskStatus
    assigned_to: Optional[UUID]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    compliance_score: int
    completed_at: Optional[datetime]
    is_active: bool
    version: int
    created_at: datetime
    updated_at: datetime
    
    # Nested relationships
    creator: Optional[UserResponse] = None
    assignee: Optional[UserResponse] = None


class TaskListResponse(ConstitutionalBaseSchema):
    """Schema for paginated task list responses"""
    tasks: List[TaskResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


# Audit log schemas
class AuditLogResponse(ConstitutionalBaseSchema):
    """Schema for audit log responses"""
    id: UUID
    action: str
    entity_type: str
    entity_id: UUID
    user_id: Optional[UUID]
    timestamp: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    old_values: Optional[Dict[str, Any]]
    new_values: Optional[Dict[str, Any]]
    changes_summary: Optional[str]
    constitutional_score: int
    violation_flags: List[str]


# Constitutional rule schemas
class ConstitutionalRuleBase(ConstitutionalBaseSchema):
    """Base constitutional rule schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    rule_type: str = Field(..., description="Type of rule (validation, security, business)")
    rule_expression: str = Field(..., description="Rule expression in JSON or other format")
    severity: str = Field(default="medium", regex="^(low|medium|high|critical)$")
    applies_to_entity: Optional[str] = None
    applies_to_action: Optional[str] = None
    is_enabled: bool = Field(default=True)
    enforcement_mode: str = Field(default="strict", regex="^(strict|warning|advisory)$")
    tags: Optional[List[str]] = Field(default_factory=list)
    metadata_json: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ConstitutionalRuleCreate(ConstitutionalRuleBase):
    """Schema for creating constitutional rules"""
    pass


class ConstitutionalRuleUpdate(ConstitutionalBaseSchema):
    """Schema for updating constitutional rules"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    rule_type: Optional[str] = None
    rule_expression: Optional[str] = None
    severity: Optional[str] = Field(None, regex="^(low|medium|high|critical)$")
    applies_to_entity: Optional[str] = None
    applies_to_action: Optional[str] = None
    is_enabled: Optional[bool] = None
    enforcement_mode: Optional[str] = Field(None, regex="^(strict|warning|advisory)$")
    tags: Optional[List[str]] = None
    metadata_json: Optional[Dict[str, Any]] = None


class ConstitutionalRuleResponse(ConstitutionalRuleBase):
    """Schema for constitutional rule responses"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    is_active: bool
    version: int


# Authentication schemas
class Token(ConstitutionalBaseSchema):
    """JWT token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class TokenData(ConstitutionalBaseSchema):
    """Token data for JWT validation"""
    username: Optional[str] = None
    user_id: Optional[UUID] = None
    role: Optional[UserRole] = None
    exp: Optional[datetime] = None


# Health check and system schemas
class HealthCheck(ConstitutionalBaseSchema):
    """Health check response schema"""
    status: str = "healthy"
    timestamp: datetime
    version: str
    database: str = "connected"
    constitutional_score: int = 100


# Error schemas
class ErrorResponse(ConstitutionalBaseSchema):
    """Standardized error response schema"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    constitutional_violations: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = None


class ValidationErrorResponse(ErrorResponse):
    """Validation error response schema"""
    field_errors: Optional[Dict[str, List[str]]] = None


# Query parameter schemas
class TaskFilterParams(ConstitutionalBaseSchema):
    """Query parameters for filtering tasks"""
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[UUID] = None
    created_by: Optional[UUID] = None
    tags: Optional[str] = None  # Comma-separated tags
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    created_after: Optional[datetime] = None
    search: Optional[str] = None  # Search in title and description
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", regex="^(asc|desc)$")


class UserFilterParams(ConstitutionalBaseSchema):
    """Query parameters for filtering users"""
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    search: Optional[str] = None  # Search in username, email, full_name
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", regex="^(asc|desc)$")
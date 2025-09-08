"""
Database models for Constitutional APIs
Implements the constitutional architecture principles with built-in validation and security
"""

from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    String,
    Text,
    DateTime,
    Integer,
    Enum as SQLEnum,
    ForeignKey,
    JSON,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from src.database import Base


class TaskStatus(str, enum.Enum):
    """Constitutional task status enum"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, enum.Enum):
    """Constitutional task priority enum"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UserRole(str, enum.Enum):
    """Constitutional user role enum"""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


# Base model with constitutional principles
class ConstitutionalBase(Base):
    """
    Abstract base class implementing constitutional principles:
    - Immutable audit trail
    - Automatic timestamps
    - UUID-based identification
    - Built-in validation
    """
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    version = Column(Integer, default=1, nullable=False)


class User(ConstitutionalBase):
    """
    Constitutional User model with built-in security and validation
    """
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_token = Column(String(255), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    password_changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Constitutional metadata
    metadata_json = Column(JSON, default=dict)

    # Relationships
    created_tasks = relationship("Task", foreign_keys="Task.created_by", back_populates="creator")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
    audit_logs = relationship("AuditLog", back_populates="user")

    # Indexes for performance
    __table_args__ = (
        Index("idx_user_email_active", "email", "is_active"),
        Index("idx_user_username_active", "username", "is_active"),
        Index("idx_user_role_active", "role", "is_active"),
    )


class Task(ConstitutionalBase):
    """
    Constitutional Task model representing work items with built-in validation
    """
    __tablename__ = "tasks"

    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False, index=True)
    
    # Assignment and ownership
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Constitutional validation rules
    validation_rules = Column(JSON, default=dict)
    compliance_score = Column(Integer, default=0, nullable=False)
    
    # Metadata and tags
    tags = Column(JSON, default=list)
    metadata_json = Column(JSON, default=dict)
    
    # Relationships
    creator = relationship("User", foreign_keys="Task.created_by", back_populates="created_tasks")
    assignee = relationship("User", foreign_keys="Task.assigned_to", back_populates="assigned_tasks")
    audit_logs = relationship("AuditLog", back_populates="task")

    # Constraints and indexes
    __table_args__ = (
        Index("idx_task_status_priority", "status", "priority"),
        Index("idx_task_assigned_status", "assigned_to", "status"),
        Index("idx_task_created_date", "created_at"),
        Index("idx_task_due_date", "due_date"),
    )

    def calculate_compliance_score(self) -> int:
        """Calculate constitutional compliance score"""
        score = 0
        
        # Basic validation points
        if self.title and len(self.title.strip()) > 0:
            score += 10
        if self.description and len(self.description.strip()) > 0:
            score += 10
        if self.assigned_to:
            score += 10
        if self.due_date:
            score += 10
        if self.status != TaskStatus.PENDING:
            score += 10
            
        # Priority-based scoring
        priority_scores = {
            TaskPriority.LOW: 5,
            TaskPriority.MEDIUM: 10,
            TaskPriority.HIGH: 15,
            TaskPriority.CRITICAL: 20,
        }
        score += priority_scores.get(self.priority, 0)
        
        # Validation rules compliance
        if self.validation_rules:
            score += len(self.validation_rules) * 5
            
        return min(score, 100)  # Cap at 100


class AuditLog(ConstitutionalBase):
    """
    Constitutional Audit Log for immutable audit trail
    """
    __tablename__ = "audit_logs"

    # What happened
    action = Column(String(100), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False, index=True)
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Who did it
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    
    # When and where
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(String(500), nullable=True)
    
    # What changed
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    changes_summary = Column(Text, nullable=True)
    
    # Constitutional metadata
    constitutional_score = Column(Integer, default=0, nullable=False)
    violation_flags = Column(JSON, default=list)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    task = relationship("Task", back_populates="audit_logs", 
                       primaryjoin="and_(AuditLog.entity_id == Task.id, "
                                  "AuditLog.entity_type == 'Task')",
                       foreign_keys=[entity_id])

    # Indexes for efficient querying
    __table_args__ = (
        Index("idx_audit_entity", "entity_type", "entity_id"),
        Index("idx_audit_user_timestamp", "user_id", "timestamp"),
        Index("idx_audit_action_timestamp", "action", "timestamp"),
        Index("idx_audit_timestamp", "timestamp"),
    )


class ConstitutionalRule(ConstitutionalBase):
    """
    Constitutional Rules that define the system's behavior and validation
    """
    __tablename__ = "constitutional_rules"

    name = Column(String(200), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)
    rule_type = Column(String(50), nullable=False, index=True)  # validation, security, business, etc.
    
    # Rule definition
    rule_expression = Column(Text, nullable=False)  # JSON or expression format
    severity = Column(String(20), default="medium", nullable=False)  # low, medium, high, critical
    
    # Application scope
    applies_to_entity = Column(String(100), nullable=True, index=True)
    applies_to_action = Column(String(100), nullable=True, index=True)
    
    # Rule status
    is_enabled = Column(Boolean, default=True, nullable=False)
    enforcement_mode = Column(String(20), default="strict", nullable=False)  # strict, warning, advisory
    
    # Metadata
    tags = Column(JSON, default=list)
    metadata_json = Column(JSON, default=dict)

    # Indexes
    __table_args__ = (
        Index("idx_rule_type_enabled", "rule_type", "is_enabled"),
        Index("idx_rule_entity_action", "applies_to_entity", "applies_to_action"),
    )


# Association tables for many-to-many relationships
class TaskTag(Base):
    """Association table for task tags"""
    __tablename__ = "task_tags"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    tag = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint("task_id", "tag", name="uq_task_tag"),
        Index("idx_task_tag_tag", "tag"),
    )
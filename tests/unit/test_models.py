"""
Unit tests for constitutional database models
"""

import pytest
from datetime import datetime
from uuid import UUID

from src.models.db_models import User, Task, AuditLog, ConstitutionalRule, TaskStatus, TaskPriority, UserRole


class TestUserModel:
    """Test cases for User model"""
    
    def test_create_user(self, db_session):
        """Test creating a user with constitutional principles"""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "hashed_password": "hashed_password_here",
            "full_name": "New User",
            "role": UserRole.USER,
            "is_verified": False,
            "is_active": True
        }
        
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Verify constitutional base fields are set
        assert isinstance(user.id, UUID)
        assert user.created_at is not None
        assert user.updated_at is not None
        assert user.is_active is True
        assert user.version == 1
        
        # Verify user-specific fields
        assert user.email == "newuser@example.com"
        assert user.username == "newuser"
        assert user.role == UserRole.USER
        assert user.failed_login_attempts == 0
    
    def test_user_relationships(self, db_session, test_user):
        """Test user model relationships"""
        # Create a task for the user
        task = Task(
            title="Test Task",
            description="Test task description",
            created_by=test_user.id,
            assigned_to=test_user.id,
            priority=TaskPriority.MEDIUM
        )
        db_session.add(task)
        db_session.commit()
        
        # Verify relationships work
        db_session.refresh(test_user)
        assert len(test_user.created_tasks) > 0
        assert len(test_user.assigned_tasks) > 0
        assert test_user.created_tasks[0].title == "Test Task"


class TestTaskModel:
    """Test cases for Task model"""
    
    def test_create_task(self, db_session, test_user):
        """Test creating a task with constitutional principles"""
        task = Task(
            title="Constitutional Test Task",
            description="A task to test constitutional compliance",
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING,
            created_by=test_user.id,
            assigned_to=test_user.id,
            tags=["test", "constitutional"],
            metadata_json={"category": "testing"},
            validation_rules={"required": ["title", "description"]}
        )
        
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        # Verify constitutional base fields
        assert isinstance(task.id, UUID)
        assert task.created_at is not None
        assert task.updated_at is not None
        assert task.is_active is True
        assert task.version == 1
        
        # Verify task-specific fields
        assert task.title == "Constitutional Test Task"
        assert task.priority == TaskPriority.HIGH
        assert task.status == TaskStatus.PENDING
        assert task.tags == ["test", "constitutional"]
        assert task.validation_rules == {"required": ["title", "description"]}
    
    def test_task_compliance_score_calculation(self, db_session, test_user):
        """Test constitutional compliance score calculation"""
        # Create task with minimal data
        minimal_task = Task(
            title="Minimal Task",
            created_by=test_user.id
        )
        minimal_score = minimal_task.calculate_compliance_score()
        
        # Create task with comprehensive data
        comprehensive_task = Task(
            title="Comprehensive Constitutional Task",
            description="Detailed description of the task requirements and objectives",
            priority=TaskPriority.CRITICAL,
            status=TaskStatus.IN_PROGRESS,
            assigned_to=test_user.id,
            created_by=test_user.id,
            validation_rules={"required": ["title", "description"], "format": "standard"}
        )
        comprehensive_score = comprehensive_task.calculate_compliance_score()
        
        # Comprehensive task should have higher score
        assert comprehensive_score > minimal_score
        assert comprehensive_score <= 100  # Score should be capped at 100
        assert minimal_score >= 0  # Score should not be negative
    
    def test_task_status_transitions(self, db_session, test_user):
        """Test task status transitions"""
        task = Task(
            title="Status Test Task",
            status=TaskStatus.PENDING,
            created_by=test_user.id
        )
        
        db_session.add(task)
        db_session.commit()
        
        # Verify initial status
        assert task.status == TaskStatus.PENDING
        assert task.completed_at is None
        
        # Update to completed
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        db_session.commit()
        
        # Verify completion
        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at is not None


class TestAuditLogModel:
    """Test cases for AuditLog model"""
    
    def test_create_audit_log(self, db_session, test_user):
        """Test creating an audit log entry"""
        audit_log = AuditLog(
            action="CREATE",
            entity_type="Task",
            entity_id=test_user.id,  # Using user id as placeholder
            user_id=test_user.id,
            timestamp=datetime.utcnow(),
            old_values={"status": "pending"},
            new_values={"status": "in_progress"},
            changes_summary="Status updated from pending to in_progress",
            constitutional_score=85,
            violation_flags=[]
        )
        
        db_session.add(audit_log)
        db_session.commit()
        db_session.refresh(audit_log)
        
        # Verify audit log fields
        assert isinstance(audit_log.id, UUID)
        assert audit_log.action == "CREATE"
        assert audit_log.entity_type == "Task"
        assert audit_log.user_id == test_user.id
        assert audit_log.constitutional_score == 85
        assert audit_log.violation_flags == []
        assert audit_log.old_values == {"status": "pending"}
        assert audit_log.new_values == {"status": "in_progress"}


class TestConstitutionalRuleModel:
    """Test cases for ConstitutionalRule model"""
    
    def test_create_constitutional_rule(self, db_session, test_user):
        """Test creating a constitutional rule"""
        rule = ConstitutionalRule(
            name="Task Title Validation",
            description="Validates that task titles are meaningful and descriptive",
            rule_type="validation",
            rule_expression='{"min_length": 5, "max_length": 200, "required": true}',
            severity="medium",
            applies_to_entity="Task",
            applies_to_action="CREATE",
            is_enabled=True,
            enforcement_mode="strict",
            tags=["validation", "title"],
            created_by=test_user.id
        )
        
        db_session.add(rule)
        db_session.commit()
        db_session.refresh(rule)
        
        # Verify rule fields
        assert isinstance(rule.id, UUID)
        assert rule.name == "Task Title Validation"
        assert rule.rule_type == "validation"
        assert rule.severity == "medium"
        assert rule.is_enabled is True
        assert rule.enforcement_mode == "strict"
        assert "validation" in rule.tags


class TestConstitutionalBase:
    """Test cases for constitutional base functionality"""
    
    def test_constitutional_timestamps(self, db_session, test_user):
        """Test that constitutional base automatically handles timestamps"""
        initial_time = datetime.utcnow()
        
        # Create task
        task = Task(
            title="Timestamp Test",
            created_by=test_user.id
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        # Verify timestamps are set
        assert task.created_at is not None
        assert task.updated_at is not None
        assert task.created_at >= initial_time
        assert task.updated_at >= initial_time
        
        # Update task
        original_created = task.created_at
        original_updated = task.updated_at
        
        task.title = "Updated Timestamp Test"
        task.version += 1
        db_session.commit()
        db_session.refresh(task)
        
        # Verify updated_at changed but created_at didn't
        assert task.created_at == original_created
        assert task.updated_at > original_updated
    
    def test_constitutional_versioning(self, db_session, test_user):
        """Test constitutional versioning system"""
        task = Task(
            title="Version Test",
            created_by=test_user.id
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        # Verify initial version
        assert task.version == 1
        
        # Update and increment version
        task.title = "Updated Version Test"
        task.version += 1
        db_session.commit()
        db_session.refresh(task)
        
        # Verify version incremented
        assert task.version == 2
    
    def test_soft_deletion(self, db_session, test_user):
        """Test constitutional soft deletion"""
        task = Task(
            title="Deletion Test",
            created_by=test_user.id,
            is_active=True
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        # Verify initially active
        assert task.is_active is True
        
        # Soft delete
        task.is_active = False
        task.version += 1
        db_session.commit()
        
        # Verify soft deletion
        assert task.is_active is False
        
        # Verify task still exists in database
        deleted_task = db_session.query(Task).filter(Task.id == task.id).first()
        assert deleted_task is not None
        assert deleted_task.is_active is False
"""
Integration tests for constitutional task API endpoints
"""

import pytest
from datetime import datetime, timedelta
from fastapi import status

from src.models.db_models import Task, TaskStatus, TaskPriority


class TestTaskEndpoints:
    """Test cases for task API endpoints"""
    
    def test_create_task_success(self, client, auth_headers, test_task_data):
        """Test successful task creation"""
        response = client.post("/api/tasks/", json=test_task_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["title"] == test_task_data["title"]
        assert data["description"] == test_task_data["description"]
        assert data["priority"] == test_task_data["priority"]
        assert data["status"] == "pending"  # Default status
        assert data["tags"] == test_task_data["tags"]
        assert data["compliance_score"] > 0  # Should have constitutional compliance score
        assert "id" in data
        assert "created_at" in data
    
    def test_create_task_unauthorized(self, client, test_task_data):
        """Test task creation without authentication"""
        response = client.post("/api/tasks/", json=test_task_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_task_invalid_data(self, client, auth_headers):
        """Test task creation with invalid data"""
        invalid_data = {
            "title": "",  # Empty title
            "priority": "invalid_priority",
            "due_date": "invalid_date"
        }
        
        response = client.post("/api/tasks/", json=invalid_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_task_with_assignment(self, client, auth_headers, test_user, test_task_data):
        """Test task creation with user assignment"""
        test_task_data["assigned_to"] = str(test_user.id)
        
        response = client.post("/api/tasks/", json=test_task_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["assigned_to"] == str(test_user.id)
    
    def test_create_task_invalid_assignment(self, client, auth_headers, test_task_data):
        """Test task creation with invalid user assignment"""
        from uuid import uuid4
        test_task_data["assigned_to"] = str(uuid4())  # Non-existent user
        
        response = client.post("/api/tasks/", json=test_task_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "not found" in response.json()["detail"]
    
    def test_list_tasks_success(self, client, auth_headers, db_session, test_user, test_task_data):
        """Test successful task listing"""
        # Create test tasks
        task1 = Task(title="Task 1", created_by=test_user.id)
        task2 = Task(title="Task 2", created_by=test_user.id, assigned_to=test_user.id)
        db_session.add_all([task1, task2])
        db_session.commit()
        
        response = client.get("/api/tasks/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert "page" in data
        assert "per_page" in data
        assert data["total"] >= 2
        assert len(data["tasks"]) >= 2
    
    def test_list_tasks_with_filters(self, client, auth_headers, db_session, test_user):
        """Test task listing with filters"""
        # Create tasks with different statuses
        task1 = Task(title="Pending Task", status=TaskStatus.PENDING, created_by=test_user.id)
        task2 = Task(title="In Progress Task", status=TaskStatus.IN_PROGRESS, created_by=test_user.id)
        db_session.add_all([task1, task2])
        db_session.commit()
        
        # Filter by status
        response = client.get("/api/tasks/?status=pending", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert all(task["status"] == "pending" for task in data["tasks"])
        
        # Filter by priority
        task1.priority = TaskPriority.HIGH
        db_session.commit()
        
        response = client.get("/api/tasks/?priority=high", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
    
    def test_list_tasks_pagination(self, client, auth_headers, db_session, test_user):
        """Test task listing pagination"""
        # Create multiple tasks
        tasks = [Task(title=f"Task {i}", created_by=test_user.id) for i in range(5)]
        db_session.add_all(tasks)
        db_session.commit()
        
        # Test pagination
        response = client.get("/api/tasks/?page=1&per_page=2", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert len(data["tasks"]) <= 2
        assert data["page"] == 1
        assert data["per_page"] == 2
        assert data["has_next"] or data["has_prev"] or data["total"] <= 2
    
    def test_get_task_success(self, client, auth_headers, db_session, test_user):
        """Test getting a specific task"""
        task = Task(title="Get Task Test", created_by=test_user.id)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        response = client.get(f"/api/tasks/{task.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == str(task.id)
        assert data["title"] == "Get Task Test"
    
    def test_get_task_not_found(self, client, auth_headers):
        """Test getting non-existent task"""
        from uuid import uuid4
        non_existent_id = uuid4()
        
        response = client.get(f"/api/tasks/{non_existent_id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_task_access_control(self, client, db_session, test_user_data):
        """Test task access control between users"""
        from src.models.db_models import User, UserRole
        from src.auth import auth
        
        # Create two users
        user1 = User(
            email="user1@example.com",
            username="user1",
            hashed_password=auth.get_password_hash("Password123!"),
            role=UserRole.USER,
            is_verified=True,
            is_active=True
        )
        user2 = User(
            email="user2@example.com",
            username="user2",
            hashed_password=auth.get_password_hash("Password123!"),
            role=UserRole.USER,
            is_verified=True,
            is_active=True
        )
        db_session.add_all([user1, user2])
        db_session.commit()
        db_session.refresh(user1)
        db_session.refresh(user2)
        
        # Create task for user1
        task = Task(title="Private Task", created_by=user1.id)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        # Create token for user2
        token_data = {
            "sub": user2.username,
            "user_id": str(user2.id),
            "role": user2.role.value,
            "email": user2.email
        }
        user2_token = auth.create_access_token(data=token_data)
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        # User2 should not be able to access user1's task
        response = client.get(f"/api/tasks/{task.id}", headers=user2_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_task_success(self, client, auth_headers, db_session, test_user):
        """Test successful task update"""
        task = Task(title="Original Title", created_by=test_user.id)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "status": "in_progress"
        }
        
        response = client.put(f"/api/tasks/{task.id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"
        assert data["status"] == "in_progress"
        assert data["version"] == 2  # Version should increment
    
    def test_update_task_not_found(self, client, auth_headers):
        """Test updating non-existent task"""
        from uuid import uuid4
        non_existent_id = uuid4()
        
        update_data = {"title": "Updated"}
        response = client.put(f"/api/tasks/{non_existent_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_task_success(self, client, auth_headers, db_session, test_user):
        """Test successful task deletion (soft delete)"""
        task = Task(title="To Delete", created_by=test_user.id)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        response = client.delete(f"/api/tasks/{task.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify task is soft deleted
        db_session.refresh(task)
        assert task.is_active is False
    
    def test_complete_task_success(self, client, auth_headers, db_session, test_user):
        """Test task completion"""
        task = Task(title="To Complete", created_by=test_user.id, assigned_to=test_user.id)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        response = client.post(f"/api/tasks/{task.id}/complete", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["status"] == "completed"
        assert data["completed_at"] is not None
    
    def test_complete_task_access_control(self, client, db_session, test_user_data):
        """Test task completion access control"""
        from src.models.db_models import User, UserRole
        from src.auth import auth
        
        # Create two users
        user1 = User(
            email="creator@example.com",
            username="creator",
            hashed_password=auth.get_password_hash("Password123!"),
            role=UserRole.USER,
            is_verified=True,
            is_active=True
        )
        user2 = User(
            email="assignee@example.com",
            username="assignee",
            hashed_password=auth.get_password_hash("Password123!"),
            role=UserRole.USER,
            is_verified=True,
            is_active=True
        )
        db_session.add_all([user1, user2])
        db_session.commit()
        db_session.refresh(user1)
        db_session.refresh(user2)
        
        # Create task created by user1, assigned to user2
        task = Task(title="Assigned Task", created_by=user1.id, assigned_to=user2.id)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        # Create token for user1 (creator, not assignee)
        user1_token = auth.create_access_token(data={
            "sub": user1.username,
            "user_id": str(user1.id),
            "role": user1.role.value,
            "email": user1.email
        })
        user1_headers = {"Authorization": f"Bearer {user1_token}"}
        
        # User1 (creator) should not be able to complete task assigned to user2
        response = client.post(f"/api/tasks/{task.id}/complete", headers=user1_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestTaskValidation:
    """Test task validation and constitutional compliance"""
    
    def test_task_title_validation(self, client, auth_headers):
        """Test task title validation"""
        invalid_titles = ["", "   ", None]
        
        for title in invalid_titles:
            task_data = {"title": title, "description": "Valid description"}
            response = client.post("/api/tasks/", json=task_data, headers=auth_headers)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_task_priority_validation(self, client, auth_headers):
        """Test task priority validation"""
        task_data = {
            "title": "Valid Title",
            "priority": "invalid_priority"
        }
        
        response = client.post("/api/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_task_due_date_validation(self, client, auth_headers):
        """Test due date validation (must be in future)"""
        from datetime import datetime, timedelta
        
        past_date = (datetime.now() - timedelta(days=1)).isoformat()
        task_data = {
            "title": "Valid Title",
            "due_date": past_date
        }
        
        response = client.post("/api/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_task_constitutional_compliance_scoring(self, client, auth_headers, db_session):
        """Test constitutional compliance scoring"""
        # Create minimal task
        minimal_task = {
            "title": "Min"
        }
        
        response = client.post("/api/tasks/", json=minimal_task, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        minimal_score = response.json()["compliance_score"]
        
        # Create comprehensive task
        comprehensive_task = {
            "title": "Comprehensive Constitutional Task",
            "description": "Detailed description with all required fields",
            "priority": "high",
            "tags": ["constitutional", "comprehensive"],
            "metadata_json": {"category": "important"},
            "validation_rules": {"required": ["title", "description"]}
        }
        
        response = client.post("/api/tasks/", json=comprehensive_task, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        comprehensive_score = response.json()["compliance_score"]
        
        # Comprehensive task should have higher compliance score
        assert comprehensive_score > minimal_score
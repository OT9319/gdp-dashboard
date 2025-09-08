"""
Constitutional Task Routes
Implements task management endpoints with constitutional validation and security
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc

from src.database import get_db
from src.models.db_models import Task, User, TaskStatus, TaskPriority, AuditLog
from src.models.schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    TaskFilterParams, ErrorResponse
)
from src.auth import get_current_verified_user, require_admin, require_moderator
from src.middleware.audit import log_audit_event

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new constitutional task",
    description="Create a new task with constitutional validation and audit logging"
)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Create a new constitutional task with comprehensive validation
    """
    try:
        # Constitutional validation
        if task_data.assigned_to:
            assigned_user = db.query(User).filter(
                User.id == task_data.assigned_to,
                User.is_active == True
            ).first()
            if not assigned_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Assigned user not found or inactive"
                )
        
        # Create task with constitutional principles
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            assigned_to=task_data.assigned_to,
            due_date=task_data.due_date,
            tags=task_data.tags or [],
            metadata_json=task_data.metadata_json or {},
            validation_rules=task_data.validation_rules or {},
            created_by=current_user.id,
            updated_by=current_user.id
        )
        
        # Calculate constitutional compliance score
        db_task.compliance_score = db_task.calculate_compliance_score()
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        # Log audit event
        await log_audit_event(
            db=db,
            action="CREATE",
            entity_type="Task",
            entity_id=db_task.id,
            user_id=current_user.id,
            new_values=task_data.dict(),
            constitutional_score=db_task.compliance_score
        )
        
        return TaskResponse.from_orm(db_task)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get(
    "/",
    response_model=TaskListResponse,
    summary="List constitutional tasks",
    description="Retrieve tasks with constitutional filtering and pagination"
)
async def list_tasks(
    filter_params: TaskFilterParams = Depends(),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
) -> TaskListResponse:
    """
    List tasks with constitutional filtering, pagination, and access control
    """
    try:
        # Build base query with constitutional principles
        query = db.query(Task).filter(Task.is_active == True)
        
        # Apply filters
        if filter_params.status:
            query = query.filter(Task.status == filter_params.status)
        
        if filter_params.priority:
            query = query.filter(Task.priority == filter_params.priority)
        
        if filter_params.assigned_to:
            query = query.filter(Task.assigned_to == filter_params.assigned_to)
        
        if filter_params.created_by:
            query = query.filter(Task.created_by == filter_params.created_by)
        
        if filter_params.tags:
            # Parse comma-separated tags
            tag_list = [tag.strip() for tag in filter_params.tags.split(",")]
            query = query.filter(Task.tags.op("&&")(tag_list))
        
        if filter_params.due_before:
            query = query.filter(Task.due_date <= filter_params.due_before)
        
        if filter_params.due_after:
            query = query.filter(Task.due_date >= filter_params.due_after)
        
        if filter_params.created_before:
            query = query.filter(Task.created_at <= filter_params.created_before)
        
        if filter_params.created_after:
            query = query.filter(Task.created_at >= filter_params.created_after)
        
        if filter_params.search:
            search_term = f"%{filter_params.search}%"
            query = query.filter(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term)
                )
            )
        
        # Apply constitutional access control
        # Users can see tasks they created or are assigned to, admins can see all
        if current_user.role.value not in ["admin", "moderator"]:
            query = query.filter(
                or_(
                    Task.created_by == current_user.id,
                    Task.assigned_to == current_user.id
                )
            )
        
        # Count total results
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(Task, filter_params.sort_by, Task.created_at)
        if filter_params.sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        # Apply pagination
        offset = (filter_params.page - 1) * filter_params.per_page
        tasks = query.offset(offset).limit(filter_params.per_page).all()
        
        # Calculate pagination info
        pages = (total + filter_params.per_page - 1) // filter_params.per_page
        has_next = filter_params.page < pages
        has_prev = filter_params.page > 1
        
        return TaskListResponse(
            tasks=[TaskResponse.from_orm(task) for task in tasks],
            total=total,
            page=filter_params.page,
            per_page=filter_params.per_page,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}"
        )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get constitutional task by ID",
    description="Retrieve a specific task with constitutional access control"
)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Get a specific task with constitutional access control
    """
    try:
        # Query task with constitutional principles
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.is_active == True
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Constitutional access control
        if current_user.role.value not in ["admin", "moderator"]:
            if task.created_by != current_user.id and task.assigned_to != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to this task"
                )
        
        return TaskResponse.from_orm(task)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve task: {str(e)}"
        )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update constitutional task",
    description="Update a task with constitutional validation and audit logging"
)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Update a task with constitutional validation and audit trail
    """
    try:
        # Get existing task
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.is_active == True
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Constitutional access control
        if current_user.role.value not in ["admin", "moderator"]:
            if task.created_by != current_user.id and task.assigned_to != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to update this task"
                )
        
        # Store old values for audit
        old_values = {
            "title": task.title,
            "description": task.description,
            "status": task.status.value if task.status else None,
            "priority": task.priority.value if task.priority else None,
            "assigned_to": str(task.assigned_to) if task.assigned_to else None,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "tags": task.tags,
            "metadata_json": task.metadata_json,
        }
        
        # Apply updates
        update_data = task_update.dict(exclude_unset=True)
        
        # Validate assigned user if provided
        if "assigned_to" in update_data and update_data["assigned_to"]:
            assigned_user = db.query(User).filter(
                User.id == update_data["assigned_to"],
                User.is_active == True
            ).first()
            if not assigned_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Assigned user not found or inactive"
                )
        
        # Update fields
        for field, value in update_data.items():
            if hasattr(task, field) and value is not None:
                setattr(task, field, value)
        
        # Update metadata
        task.updated_by = current_user.id
        task.version += 1
        
        # Recalculate compliance score
        task.compliance_score = task.calculate_compliance_score()
        
        # Handle status changes
        if task_update.status == TaskStatus.COMPLETED and not task.completed_at:
            task.completed_at = datetime.utcnow()
        elif task_update.status != TaskStatus.COMPLETED and task.completed_at:
            task.completed_at = None
        
        db.commit()
        db.refresh(task)
        
        # Log audit event
        new_values = {
            "title": task.title,
            "description": task.description,
            "status": task.status.value if task.status else None,
            "priority": task.priority.value if task.priority else None,
            "assigned_to": str(task.assigned_to) if task.assigned_to else None,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "tags": task.tags,
            "metadata_json": task.metadata_json,
        }
        
        await log_audit_event(
            db=db,
            action="UPDATE",
            entity_type="Task",
            entity_id=task.id,
            user_id=current_user.id,
            old_values=old_values,
            new_values=new_values,
            constitutional_score=task.compliance_score
        )
        
        return TaskResponse.from_orm(task)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete constitutional task",
    description="Soft delete a task with constitutional audit logging"
)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Soft delete a task with constitutional audit trail
    """
    try:
        # Get task
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.is_active == True
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Constitutional access control
        if current_user.role.value not in ["admin", "moderator"]:
            if task.created_by != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to delete this task"
                )
        
        # Soft delete
        task.is_active = False
        task.updated_by = current_user.id
        task.version += 1
        
        db.commit()
        
        # Log audit event
        await log_audit_event(
            db=db,
            action="DELETE",
            entity_type="Task",
            entity_id=task.id,
            user_id=current_user.id,
            old_values={"is_active": True},
            new_values={"is_active": False},
            constitutional_score=0  # Deletion affects compliance
        )
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        )


@router.post(
    "/{task_id}/complete",
    response_model=TaskResponse,
    summary="Complete constitutional task",
    description="Mark a task as completed with constitutional validation"
)
async def complete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Mark a task as completed with constitutional validation
    """
    try:
        # Get task
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.is_active == True
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Constitutional access control
        if current_user.role.value not in ["admin", "moderator"]:
            if task.assigned_to != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only assigned user can complete this task"
                )
        
        # Update task
        old_status = task.status
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        task.updated_by = current_user.id
        task.version += 1
        task.compliance_score = task.calculate_compliance_score()
        
        db.commit()
        db.refresh(task)
        
        # Log audit event
        await log_audit_event(
            db=db,
            action="COMPLETE",
            entity_type="Task",
            entity_id=task.id,
            user_id=current_user.id,
            old_values={"status": old_status.value, "completed_at": None},
            new_values={
                "status": task.status.value,
                "completed_at": task.completed_at.isoformat()
            },
            constitutional_score=task.compliance_score
        )
        
        return TaskResponse.from_orm(task)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete task: {str(e)}"
        )
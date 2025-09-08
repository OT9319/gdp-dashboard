"""
Constitutional Audit Middleware
Provides audit logging functionality for constitutional compliance
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from sqlalchemy.orm import Session

from src.models.db_models import AuditLog


async def log_audit_event(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: UUID,
    user_id: Optional[UUID] = None,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None,
    changes_summary: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    constitutional_score: int = 0,
    violation_flags: Optional[List[str]] = None
) -> AuditLog:
    """
    Log an audit event with constitutional compliance scoring
    """
    try:
        # Calculate constitutional score if not provided
        if constitutional_score == 0:
            constitutional_score = calculate_constitutional_score(
                action, entity_type, old_values, new_values
            )
        
        # Detect potential violations
        if violation_flags is None:
            violation_flags = detect_constitutional_violations(
                action, entity_type, old_values, new_values
            )
        
        # Create audit log entry
        audit_log = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            timestamp=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent,
            old_values=old_values or {},
            new_values=new_values or {},
            changes_summary=changes_summary or generate_changes_summary(old_values, new_values),
            constitutional_score=constitutional_score,
            violation_flags=violation_flags or [],
            created_by=user_id,
            updated_by=user_id
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        
        return audit_log
        
    except Exception as e:
        db.rollback()
        # Log error but don't fail the main operation
        print(f"Failed to log audit event: {str(e)}")
        return None


def calculate_constitutional_score(
    action: str,
    entity_type: str,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None
) -> int:
    """
    Calculate constitutional compliance score for an audit event
    """
    score = 50  # Base score
    
    # Action-based scoring
    action_scores = {
        "CREATE": 20,
        "UPDATE": 15,
        "DELETE": -10,
        "LOGIN": 10,
        "LOGOUT": 5,
        "COMPLETE": 25,
        "APPROVE": 20,
        "REJECT": 10,
    }
    score += action_scores.get(action.upper(), 0)
    
    # Entity-based scoring
    entity_scores = {
        "Task": 10,
        "User": 15,
        "ConstitutionalRule": 25,
        "AuditLog": 5,
    }
    score += entity_scores.get(entity_type, 0)
    
    # Data quality scoring
    if new_values:
        # Reward comprehensive data
        score += min(len(new_values), 15)
        
        # Reward specific good practices
        if "validation_rules" in new_values and new_values["validation_rules"]:
            score += 10
        if "due_date" in new_values and new_values["due_date"]:
            score += 5
        if "assigned_to" in new_values and new_values["assigned_to"]:
            score += 5
    
    # Change tracking scoring
    if old_values and new_values:
        # Reward tracking changes
        score += 5
        
        # Detect and score improvements
        if "status" in old_values and "status" in new_values:
            if (old_values["status"] == "pending" and 
                new_values["status"] in ["in_progress", "completed"]):
                score += 10
    
    return max(0, min(100, score))  # Clamp between 0 and 100


def detect_constitutional_violations(
    action: str,
    entity_type: str,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None
) -> List[str]:
    """
    Detect potential constitutional violations in an audit event
    """
    violations = []
    
    # Detect unauthorized deletions
    if action.upper() == "DELETE" and entity_type in ["User", "ConstitutionalRule"]:
        violations.append("CRITICAL_ENTITY_DELETION")
    
    # Detect privilege escalation
    if (old_values and new_values and 
        "role" in old_values and "role" in new_values):
        if (old_values["role"] in ["user", "moderator"] and 
            new_values["role"] == "admin"):
            violations.append("PRIVILEGE_ESCALATION")
    
    # Detect data corruption
    if new_values:
        # Check for empty critical fields
        critical_fields = ["title", "email", "username"]
        for field in critical_fields:
            if field in new_values and not new_values[field]:
                violations.append(f"EMPTY_CRITICAL_FIELD_{field.upper()}")
        
        # Check for suspicious data patterns
        if "title" in new_values and len(str(new_values["title"])) > 200:
            violations.append("SUSPICIOUS_TITLE_LENGTH")
        
        if "description" in new_values and len(str(new_values["description"])) > 10000:
            violations.append("SUSPICIOUS_DESCRIPTION_LENGTH")
    
    # Detect rapid operations (potential automation abuse)
    # This would require additional context about recent operations
    
    # Detect unusual patterns
    if action.upper() == "CREATE" and entity_type == "Task":
        if new_values and "assigned_to" in new_values and "created_by" in new_values:
            if new_values["assigned_to"] == new_values["created_by"]:
                violations.append("SELF_ASSIGNMENT")
    
    return violations


def generate_changes_summary(
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate a human-readable summary of changes
    """
    if not old_values and not new_values:
        return "No changes recorded"
    
    if not old_values:
        return f"Created with {len(new_values)} fields"
    
    if not new_values:
        return "Entity deleted or deactivated"
    
    changes = []
    
    # Find changed fields
    all_keys = set(old_values.keys()) | set(new_values.keys())
    
    for key in all_keys:
        old_val = old_values.get(key)
        new_val = new_values.get(key)
        
        if old_val != new_val:
            if old_val is None:
                changes.append(f"Added {key}")
            elif new_val is None:
                changes.append(f"Removed {key}")
            else:
                changes.append(f"Changed {key}")
    
    if not changes:
        return "No field changes detected"
    
    return f"Modified {len(changes)} fields: {', '.join(changes[:5])}"


class ConstitutionalAuditMiddleware:
    """
    Middleware class for constitutional audit logging
    """
    
    def __init__(self):
        self.enabled = True
        self.log_all_requests = False
        self.sensitive_fields = {
            "password", "hashed_password", "token", "secret", "key"
        }
    
    def sanitize_values(self, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove or mask sensitive values from audit logs
        """
        if not values:
            return values
        
        sanitized = {}
        for key, value in values.items():
            if any(sensitive in key.lower() for sensitive in self.sensitive_fields):
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = value
        
        return sanitized
    
    async def log_request(
        self,
        db: Session,
        method: str,
        path: str,
        user_id: Optional[UUID] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_body: Optional[Dict[str, Any]] = None,
        response_status: Optional[int] = None
    ):
        """
        Log HTTP request for audit purposes
        """
        if not self.enabled or not self.log_all_requests:
            return
        
        try:
            # Sanitize request body
            sanitized_body = self.sanitize_values(request_body) if request_body else {}
            
            await log_audit_event(
                db=db,
                action=f"HTTP_{method}",
                entity_type="Request",
                entity_id=UUID('00000000-0000-0000-0000-000000000000'),  # Placeholder
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                new_values={
                    "path": path,
                    "method": method,
                    "request_body": sanitized_body,
                    "response_status": response_status
                },
                constitutional_score=calculate_request_score(method, path, response_status)
            )
        except Exception as e:
            print(f"Failed to log request audit: {str(e)}")


def calculate_request_score(method: str, path: str, status_code: Optional[int] = None) -> int:
    """
    Calculate constitutional score for HTTP requests
    """
    score = 50  # Base score
    
    # Method-based scoring
    method_scores = {
        "GET": 5,
        "POST": 10,
        "PUT": 10,
        "PATCH": 8,
        "DELETE": 15,
    }
    score += method_scores.get(method.upper(), 0)
    
    # Path-based scoring (sensitive endpoints)
    if "/admin" in path:
        score += 20
    if "/api/tasks" in path:
        score += 10
    if "/auth" in path:
        score += 15
    
    # Status code-based scoring
    if status_code:
        if 200 <= status_code < 300:
            score += 10
        elif 400 <= status_code < 500:
            score -= 5
        elif status_code >= 500:
            score -= 15
    
    return max(0, min(100, score))
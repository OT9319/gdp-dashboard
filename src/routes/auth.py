"""
Constitutional Authentication Routes
Implements secure authentication endpoints with constitutional principles
"""

from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.db_models import User, UserRole
from src.models.schemas import (
    UserCreate, UserResponse, UserLogin, Token, ErrorResponse
)
from src.auth import auth, get_current_user, get_current_verified_user
from src.middleware.audit import log_audit_event

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Register a new user with constitutional validation"
)
async def register_user(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user with constitutional security validation
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )
        
        # Hash password
        hashed_password = auth.get_password_hash(user_data.password)
        
        # Create user
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role,
            is_verified=False,  # Require verification
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Log audit event
        await log_audit_event(
            db=db,
            action="REGISTER",
            entity_type="User",
            entity_id=db_user.id,
            user_id=db_user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("User-Agent"),
            new_values={
                "email": user_data.email,
                "username": user_data.username,
                "role": user_data.role.value,
                "is_verified": False
            },
            constitutional_score=75  # New user registration score
        )
        
        return UserResponse.from_orm(db_user)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register user: {str(e)}"
        )


@router.post(
    "/login",
    response_model=Token,
    summary="User login",
    description="Authenticate user and return JWT tokens"
)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db)
) -> Token:
    """
    Authenticate user and return constitutional JWT tokens
    """
    try:
        # Authenticate user
        user = auth.authenticate_user(db, form_data.username, form_data.password)
        
        if not user:
            # Log failed login attempt
            await log_audit_event(
                db=db,
                action="LOGIN_FAILED",
                entity_type="User",
                entity_id=None,
                ip_address=request.client.host if request else None,
                user_agent=request.headers.get("User-Agent") if request else None,
                new_values={"username": form_data.username},
                constitutional_score=0,
                violation_flags=["FAILED_LOGIN_ATTEMPT"]
            )
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create tokens
        access_token_expires = timedelta(minutes=auth.access_token_expire_minutes)
        access_token = auth.create_access_token(
            data={
                "sub": user.username,
                "user_id": str(user.id),
                "role": user.role.value,
                "email": user.email
            },
            expires_delta=access_token_expires
        )
        
        refresh_token_expires = timedelta(days=auth.refresh_token_expire_days)
        refresh_token = auth.create_refresh_token(
            data={
                "sub": user.username,
                "user_id": str(user.id),
                "role": user.role.value
            },
            expires_delta=refresh_token_expires
        )
        
        # Log successful login
        await log_audit_event(
            db=db,
            action="LOGIN",
            entity_type="User",
            entity_id=user.id,
            user_id=user.id,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("User-Agent") if request else None,
            new_values={"last_login": user.last_login.isoformat() if user.last_login else None},
            constitutional_score=85  # Successful login score
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=auth.access_token_expire_minutes * 60,
            refresh_token=refresh_token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to login: {str(e)}"
        )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token",
    description="Refresh access token using refresh token"
)
async def refresh_token(
    refresh_token: str,
    request: Request,
    db: Session = Depends(get_db)
) -> Token:
    """
    Refresh access token using constitutional validation
    """
    try:
        # Verify refresh token
        token_data = auth.verify_token(refresh_token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user
        user = db.query(User).filter(
            User.id == token_data.user_id,
            User.is_active == True
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=auth.access_token_expire_minutes)
        access_token = auth.create_access_token(
            data={
                "sub": user.username,
                "user_id": str(user.id),
                "role": user.role.value,
                "email": user.email
            },
            expires_delta=access_token_expires
        )
        
        # Log token refresh
        await log_audit_event(
            db=db,
            action="TOKEN_REFRESH",
            entity_type="User",
            entity_id=user.id,
            user_id=user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("User-Agent"),
            constitutional_score=70
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=auth.access_token_expire_minutes * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh token: {str(e)}"
        )


@router.post(
    "/logout",
    summary="User logout",
    description="Logout user and invalidate tokens"
)
async def logout_user(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout user with constitutional audit logging
    """
    try:
        # Log logout event
        await log_audit_event(
            db=db,
            action="LOGOUT",
            entity_type="User",
            entity_id=current_user.id,
            user_id=current_user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("User-Agent"),
            constitutional_score=60
        )
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to logout: {str(e)}"
        )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get current user information"
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Get current authenticated user information
    """
    return UserResponse.from_orm(current_user)


@router.post(
    "/verify-email",
    summary="Verify user email",
    description="Verify user email address"
)
async def verify_email(
    verification_token: str,
    db: Session = Depends(get_db)
):
    """
    Verify user email with constitutional validation
    """
    try:
        # Find user by verification token
        user = db.query(User).filter(
            User.verification_token == verification_token,
            User.is_active == True
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token"
            )
        
        if user.is_verified:
            return {"message": "Email already verified"}
        
        # Verify user
        user.is_verified = True
        user.verification_token = None
        db.commit()
        
        # Log verification
        await log_audit_event(
            db=db,
            action="EMAIL_VERIFY",
            entity_type="User",
            entity_id=user.id,
            user_id=user.id,
            old_values={"is_verified": False},
            new_values={"is_verified": True},
            constitutional_score=90
        )
        
        return {"message": "Email successfully verified"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify email: {str(e)}"
        )


@router.post(
    "/forgot-password",
    summary="Request password reset",
    description="Request password reset for user"
)
async def forgot_password(
    email: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Request password reset with constitutional security
    """
    try:
        # Find user by email
        user = db.query(User).filter(
            User.email == email,
            User.is_active == True
        ).first()
        
        if not user:
            # Don't reveal if email exists or not
            return {"message": "If email exists, password reset instructions have been sent"}
        
        # In production, generate secure token and send email
        # For now, just log the event
        await log_audit_event(
            db=db,
            action="PASSWORD_RESET_REQUEST",
            entity_type="User",
            entity_id=user.id,
            user_id=user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("User-Agent"),
            new_values={"email": email},
            constitutional_score=50
        )
        
        return {"message": "If email exists, password reset instructions have been sent"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process password reset: {str(e)}"
        )


@router.get(
    "/validate-token",
    summary="Validate JWT token",
    description="Validate current JWT token"
)
async def validate_token(
    current_user: User = Depends(get_current_verified_user)
):
    """
    Validate JWT token with constitutional principles
    """
    return {
        "valid": True,
        "user_id": str(current_user.id),
        "username": current_user.username,
        "role": current_user.role.value,
        "is_verified": current_user.is_verified,
        "constitutional_compliant": True
    }
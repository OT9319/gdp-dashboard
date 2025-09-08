"""
Test configuration for constitutional APIs
"""

import os
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from src.database import Base, get_db
from src.main import app
from src.models.db_models import User, UserRole
from src.auth import auth


# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test_constitutional.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


# Override the database dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine"""
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create database session for each test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client():
    """Create test client"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user_data():
    """Test user data"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPassword123!",
        "confirm_password": "TestPassword123!",
        "full_name": "Test User",
        "role": UserRole.USER
    }


@pytest.fixture
def test_admin_data():
    """Test admin user data"""
    return {
        "email": "admin@example.com",
        "username": "testadmin",
        "password": "AdminPassword123!",
        "confirm_password": "AdminPassword123!",
        "full_name": "Test Admin",
        "role": UserRole.ADMIN
    }


@pytest.fixture
def test_user(db_session):
    """Create test user in database"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": auth.get_password_hash("TestPassword123!"),
        "full_name": "Test User",
        "role": UserRole.USER,
        "is_verified": True,
        "is_active": True
    }
    
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


@pytest.fixture
def test_admin(db_session):
    """Create test admin in database"""
    admin_data = {
        "email": "admin@example.com",
        "username": "testadmin",
        "hashed_password": auth.get_password_hash("AdminPassword123!"),
        "full_name": "Test Admin",
        "role": UserRole.ADMIN,
        "is_verified": True,
        "is_active": True
    }
    
    admin = User(**admin_data)
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    
    return admin


@pytest.fixture
def user_token(test_user):
    """Create JWT token for test user"""
    token_data = {
        "sub": test_user.username,
        "user_id": str(test_user.id),
        "role": test_user.role.value,
        "email": test_user.email
    }
    return auth.create_access_token(data=token_data)


@pytest.fixture
def admin_token(test_admin):
    """Create JWT token for test admin"""
    token_data = {
        "sub": test_admin.username,
        "user_id": str(test_admin.id),
        "role": test_admin.role.value,
        "email": test_admin.email
    }
    return auth.create_access_token(data=token_data)


@pytest.fixture
def auth_headers(user_token):
    """Create authorization headers for test user"""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def admin_headers(admin_token):
    """Create authorization headers for test admin"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def test_task_data():
    """Test task data"""
    return {
        "title": "Test Task",
        "description": "This is a test task for constitutional validation",
        "priority": "medium",
        "tags": ["test", "constitutional"],
        "metadata_json": {"category": "testing"},
        "validation_rules": {"required_fields": ["title", "description"]}
    }
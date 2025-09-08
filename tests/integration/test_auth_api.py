"""
Integration tests for constitutional authentication API endpoints
"""

import pytest
from fastapi import status

from src.models.db_models import User, UserRole


class TestAuthenticationEndpoints:
    """Test cases for authentication endpoints"""
    
    def test_register_user_success(self, client, test_user_data):
        """Test successful user registration"""
        response = client.post("/api/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["username"] == test_user_data["username"]
        assert data["role"] == test_user_data["role"].value
        assert data["is_verified"] is False  # Should require verification
        assert "id" in data
        assert "created_at" in data
    
    def test_register_user_duplicate_email(self, client, test_user_data, test_user):
        """Test registration with duplicate email"""
        test_user_data["email"] = test_user.email
        test_user_data["username"] = "different_username"
        
        response = client.post("/api/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]
    
    def test_register_user_duplicate_username(self, client, test_user_data, test_user):
        """Test registration with duplicate username"""
        test_user_data["email"] = "different@example.com"
        test_user_data["username"] = test_user.username
        
        response = client.post("/api/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]
    
    def test_register_user_invalid_data(self, client):
        """Test registration with invalid data"""
        invalid_data = {
            "email": "not_an_email",
            "username": "ab",  # Too short
            "password": "weak",  # Too weak
            "confirm_password": "different",  # Doesn't match
            "role": "user"
        }
        
        response = client.post("/api/auth/register", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        login_data = {
            "username": test_user.username,
            "password": "TestPassword123!"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0
    
    def test_login_with_email(self, client, test_user):
        """Test login using email instead of username"""
        login_data = {
            "username": test_user.email,
            "password": "TestPassword123!"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "access_token" in data
    
    def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials"""
        login_data = {
            "username": test_user.username,
            "password": "WrongPassword123!"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        login_data = {
            "username": "nonexistent",
            "password": "password"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user information"""
        response = client.get("/api/auth/me", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "id" in data
        assert "username" in data
        assert "email" in data
        assert "role" in data
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_logout_success(self, client, auth_headers):
        """Test successful logout"""
        response = client.post("/api/auth/logout", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert "Successfully logged out" in response.json()["message"]
    
    def test_logout_unauthorized(self, client):
        """Test logout without authentication"""
        response = client.post("/api/auth/logout")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_validate_token_success(self, client, auth_headers):
        """Test token validation"""
        response = client.get("/api/auth/validate-token", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["valid"] is True
        assert data["constitutional_compliant"] is True
        assert "user_id" in data
        assert "username" in data
        assert "role" in data
    
    def test_validate_token_unauthorized(self, client):
        """Test token validation without token"""
        response = client.get("/api/auth/validate-token")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_verify_email_success(self, client, db_session):
        """Test email verification"""
        # Create unverified user
        user_data = {
            "email": "verify@example.com",
            "username": "verifyuser",
            "hashed_password": "hashed_password",
            "full_name": "Verify User",
            "role": UserRole.USER,
            "is_verified": False,
            "is_active": True,
            "verification_token": "test_token_123"
        }
        
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        
        # Verify email
        response = client.post("/api/auth/verify-email", params={"verification_token": "test_token_123"})
        
        assert response.status_code == status.HTTP_200_OK
        assert "successfully verified" in response.json()["message"]
        
        # Check user is verified
        db_session.refresh(user)
        assert user.is_verified is True
        assert user.verification_token is None
    
    def test_verify_email_invalid_token(self, client):
        """Test email verification with invalid token"""
        response = client.post("/api/auth/verify-email", params={"verification_token": "invalid_token"})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid verification token" in response.json()["detail"]
    
    def test_forgot_password(self, client, test_user):
        """Test password reset request"""
        response = client.post("/api/auth/forgot-password", params={"email": test_user.email})
        
        assert response.status_code == status.HTTP_200_OK
        assert "password reset instructions" in response.json()["message"]
    
    def test_forgot_password_nonexistent_email(self, client):
        """Test password reset for non-existent email"""
        response = client.post("/api/auth/forgot-password", params={"email": "nonexistent@example.com"})
        
        # Should return success message even for non-existent email (security)
        assert response.status_code == status.HTTP_200_OK
        assert "password reset instructions" in response.json()["message"]


class TestAuthenticationSecurity:
    """Test security aspects of authentication"""
    
    def test_password_complexity_validation(self, client):
        """Test that password complexity is enforced"""
        weak_passwords = [
            "short",
            "nouppercase123!",
            "NOLOWERCASE123!",
            "NoDigits!",
            "NoSpecialChars123"
        ]
        
        for password in weak_passwords:
            user_data = {
                "email": f"test_{password[:5]}@example.com",
                "username": f"test_{password[:5]}",
                "password": password,
                "confirm_password": password,
                "role": "user"
            }
            
            response = client.post("/api/auth/register", json=user_data)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_username_validation(self, client):
        """Test username validation rules"""
        invalid_usernames = ["ab", ""]  # Too short, empty
        
        for username in invalid_usernames:
            user_data = {
                "email": f"{username}@example.com",
                "username": username,
                "password": "ValidPassword123!",
                "confirm_password": "ValidPassword123!",
                "role": "user"
            }
            
            response = client.post("/api/auth/register", json=user_data)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_email_validation(self, client):
        """Test email validation"""
        invalid_emails = ["not_an_email", "@example.com", "test@", ""]
        
        for email in invalid_emails:
            user_data = {
                "email": email,
                "username": f"test_{email[:5]}",
                "password": "ValidPassword123!",
                "confirm_password": "ValidPassword123!",
                "role": "user"
            }
            
            response = client.post("/api/auth/register", json=user_data)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestTokenSecurity:
    """Test JWT token security"""
    
    def test_token_includes_constitutional_claims(self, client, test_user):
        """Test that tokens include constitutional claims"""
        login_data = {
            "username": test_user.username,
            "password": "TestPassword123!"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        assert response.status_code == status.HTTP_200_OK
        
        token = response.json()["access_token"]
        
        # Decode token to check claims
        from jose import jwt
        from src.auth import SECRET_KEY, ALGORITHM
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert payload.get("constitutional") is True
        assert payload.get("type") == "access"
        assert payload.get("sub") == test_user.username
        assert payload.get("user_id") == str(test_user.id)
        assert payload.get("role") == test_user.role.value
        assert payload.get("exp") is not None
        assert payload.get("iat") is not None
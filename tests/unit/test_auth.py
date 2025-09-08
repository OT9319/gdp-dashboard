"""
Unit tests for constitutional authentication system
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from src.auth import ConstitutionalAuthenticator, validate_password_strength
from src.models.db_models import User, UserRole


class TestConstitutionalAuthenticator:
    """Test cases for constitutional authenticator"""
    
    def test_password_hashing(self):
        """Test password hashing functionality"""
        auth = ConstitutionalAuthenticator()
        password = "TestPassword123!"
        
        # Hash password
        hashed = auth.get_password_hash(password)
        
        # Verify hash
        assert hashed != password
        assert auth.verify_password(password, hashed)
        assert not auth.verify_password("wrongpassword", hashed)
    
    def test_create_access_token(self):
        """Test access token creation"""
        auth = ConstitutionalAuthenticator()
        data = {
            "sub": "testuser",
            "user_id": str(uuid4()),
            "role": "user"
        }
        
        # Create token
        token = auth.create_access_token(data)
        
        # Verify token
        token_data = auth.verify_token(token)
        assert token_data is not None
        assert token_data.username == "testuser"
        assert token_data.user_id is not None
    
    def test_create_refresh_token(self):
        """Test refresh token creation"""
        auth = ConstitutionalAuthenticator()
        data = {
            "sub": "testuser",
            "user_id": str(uuid4()),
            "role": "user"
        }
        
        # Create refresh token
        token = auth.create_refresh_token(data)
        
        # Verify token
        token_data = auth.verify_token(token)
        assert token_data is not None
        assert token_data.username == "testuser"
    
    def test_token_expiration(self):
        """Test token expiration handling"""
        auth = ConstitutionalAuthenticator()
        data = {
            "sub": "testuser",
            "user_id": str(uuid4()),
            "role": "user"
        }
        
        # Create expired token
        expired_delta = timedelta(minutes=-1)
        token = auth.create_access_token(data, expires_delta=expired_delta)
        
        # Verify expired token
        token_data = auth.verify_token(token)
        assert token_data is None
    
    def test_invalid_token(self):
        """Test invalid token handling"""
        auth = ConstitutionalAuthenticator()
        
        # Test invalid token
        token_data = auth.verify_token("invalid_token")
        assert token_data is None
        
        # Test empty token
        token_data = auth.verify_token("")
        assert token_data is None
    
    def test_authenticate_user_success(self, db_session, test_user):
        """Test successful user authentication"""
        auth = ConstitutionalAuthenticator()
        
        # Authenticate user
        authenticated_user = auth.authenticate_user(
            db_session, 
            test_user.username, 
            "TestPassword123!"
        )
        
        assert authenticated_user is not None
        assert authenticated_user.id == test_user.id
        assert authenticated_user.failed_login_attempts == 0
    
    def test_authenticate_user_failure(self, db_session, test_user):
        """Test failed user authentication"""
        auth = ConstitutionalAuthenticator()
        
        # Try to authenticate with wrong password
        authenticated_user = auth.authenticate_user(
            db_session, 
            test_user.username, 
            "WrongPassword123!"
        )
        
        assert authenticated_user is None
        
        # Check failed login attempts incremented
        db_session.refresh(test_user)
        assert test_user.failed_login_attempts > 0
    
    def test_authenticate_nonexistent_user(self, db_session):
        """Test authentication of non-existent user"""
        auth = ConstitutionalAuthenticator()
        
        authenticated_user = auth.authenticate_user(
            db_session, 
            "nonexistent", 
            "password"
        )
        
        assert authenticated_user is None


class TestPasswordValidation:
    """Test cases for password validation"""
    
    def test_valid_passwords(self):
        """Test valid password patterns"""
        valid_passwords = [
            "Password123!",
            "MySecure123@",
            "TestPass456#",
            "Strong987$"
        ]
        
        for password in valid_passwords:
            assert validate_password_strength(password), f"Password {password} should be valid"
    
    def test_invalid_passwords(self):
        """Test invalid password patterns"""
        invalid_passwords = [
            "short",
            "nouppercase123!",
            "NOLOWERCASE123!",
            "NoDigits!",
            "NoSpecialChars123",
            "12345678",
            ""
        ]
        
        for password in invalid_passwords:
            assert not validate_password_strength(password), f"Password {password} should be invalid"
    
    def test_password_edge_cases(self):
        """Test password edge cases"""
        # Exactly 8 characters, all requirements
        assert validate_password_strength("Test123!")
        
        # Very long password
        long_password = "Test123!" * 10
        assert validate_password_strength(long_password)
        
        # Unicode characters
        unicode_password = "Tëst123!"
        assert validate_password_strength(unicode_password)


class TestConstitutionalSecurity:
    """Test constitutional security principles"""
    
    def test_token_constitutional_claims(self):
        """Test that tokens include constitutional claims"""
        auth = ConstitutionalAuthenticator()
        data = {"sub": "testuser", "user_id": str(uuid4()), "role": "user"}
        
        token = auth.create_access_token(data)
        
        # Decode token manually to check claims
        from jose import jwt
        payload = jwt.decode(token, auth.secret_key, algorithms=[auth.algorithm])
        
        assert payload.get("constitutional") is True
        assert payload.get("type") == "access"
        assert payload.get("iat") is not None
        assert payload.get("exp") is not None
    
    def test_constitutional_user_lockout(self, db_session, test_user):
        """Test constitutional user lockout after failed attempts"""
        auth = ConstitutionalAuthenticator()
        
        # Attempt authentication 5 times with wrong password
        for i in range(5):
            authenticated_user = auth.authenticate_user(
                db_session,
                test_user.username,
                "WrongPassword"
            )
            assert authenticated_user is None
        
        # Check user is locked
        db_session.refresh(test_user)
        assert test_user.failed_login_attempts >= 5
        assert test_user.locked_until is not None
        assert test_user.locked_until > datetime.utcnow()
        
        # Attempt authentication with correct password should still fail
        authenticated_user = auth.authenticate_user(
            db_session,
            test_user.username,
            "TestPassword123!"
        )
        assert authenticated_user is None
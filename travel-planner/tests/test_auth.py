import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.auth.service import AuthService
from app.core.exceptions import ConflictException, UnauthorizedException


@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.fixture
def auth_service(mock_db):
    return AuthService(mock_db)


class TestSignup:
    async def test_signup_success(self, auth_service):
        with patch.object(auth_service.repo, "get_by_email", return_value=None), \
             patch.object(auth_service.repo, "create", return_value=MagicMock(id="user-1")):
            tokens = await auth_service.signup("test@example.com", "password123", "테스트")
            assert tokens.access_token
            assert tokens.refresh_token

    async def test_signup_duplicate_email(self, auth_service):
        with patch.object(auth_service.repo, "get_by_email", return_value=MagicMock()):
            with pytest.raises(ConflictException):
                await auth_service.signup("test@example.com", "password123", "테스트")


class TestLogin:
    async def test_login_success(self, auth_service):
        from app.core.security import hash_password
        hashed = hash_password("password123")
        mock_user = MagicMock(id="user-1", hashed_password=hashed)

        with patch.object(auth_service.repo, "get_by_email", return_value=mock_user):
            tokens = await auth_service.login("test@example.com", "password123")
            assert tokens.access_token

    async def test_login_wrong_password(self, auth_service):
        from app.core.security import hash_password
        hashed = hash_password("correct_password")
        mock_user = MagicMock(id="user-1", hashed_password=hashed)

        with patch.object(auth_service.repo, "get_by_email", return_value=mock_user):
            with pytest.raises(UnauthorizedException):
                await auth_service.login("test@example.com", "wrong_password")

    async def test_login_user_not_found(self, auth_service):
        with patch.object(auth_service.repo, "get_by_email", return_value=None):
            with pytest.raises(UnauthorizedException):
                await auth_service.login("notfound@example.com", "password123")

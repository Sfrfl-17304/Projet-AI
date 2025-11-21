import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_signup():
    """Test user signup endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/auth/signup",
            json={
                "email": "test@example.com",
                "full_name": "Test User",
                "password": "testpass123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"
        assert "id" in data
        assert "password" not in data


@pytest.mark.asyncio
async def test_login():
    """Test user login endpoint."""
    # First create a user
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post(
            "/auth/signup",
            json={
                "email": "login@example.com",
                "full_name": "Login User",
                "password": "loginpass123"
            }
        )
        
        # Then login
        response = await client.post(
            "/auth/login",
            data={
                "username": "login@example.com",
                "password": "loginpass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user():
    """Test getting current user info with valid token."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup
        await client.post(
            "/auth/signup",
            json={
                "email": "current@example.com",
                "full_name": "Current User",
                "password": "currentpass123"
            }
        )
        
        # Login to get token
        login_response = await client.post(
            "/auth/login",
            data={
                "username": "current@example.com",
                "password": "currentpass123"
            }
        )
        token = login_response.json()["access_token"]
        
        # Get current user
        response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "current@example.com"
        assert data["full_name"] == "Current User"

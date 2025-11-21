from typing import Optional
from datetime import datetime
from fastapi import HTTPException, status
from models.user import UserCreate, UserInDB, User
from services.auth_service import AuthService
from bson import ObjectId


class UserService:
    """Service for user-related operations."""
    
    def __init__(self, db):
        self.db = db
        self.users_collection = db.users
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get a user by email."""
        user_doc = await self.users_collection.find_one({"email": email})
        if user_doc:
            user_doc["id"] = str(user_doc["_id"])
            return UserInDB(**user_doc)
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        try:
            user_doc = await self.users_collection.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                user_doc["id"] = str(user_doc["_id"])
                return User(**user_doc)
            return None
        except Exception:
            return None
    
    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = await self.get_user_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user document
        user_dict = {
            "email": user_create.email,
            "full_name": user_create.full_name,
            "hashed_password": AuthService.get_password_hash(user_create.password),
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        # Insert into database
        result = await self.users_collection.insert_one(user_dict)
        
        # Return created user (without password)
        return User(
            id=str(result.inserted_id),
            email=user_create.email,
            full_name=user_create.full_name,
            created_at=user_dict["created_at"],
            is_active=True
        )
    
    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """Authenticate a user with email and password."""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user

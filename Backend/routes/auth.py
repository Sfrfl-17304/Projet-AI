from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import UserCreate, UserLogin, User, Token
from services.user_service import UserService
from services.auth_service import AuthService
from config.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_service(db=Depends(get_db)) -> UserService:
    """Dependency to get UserService instance."""
    return UserService(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """Get current authenticated user from JWT token."""
    token_data = AuthService.decode_token(token)
    user = await user_service.get_user_by_email(token_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        created_at=user.created_at,
        is_active=user.is_active
    )


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def signup(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Create a new user account.
    
    - **email**: valid email address
    - **full_name**: user's full name (2-100 characters)
    - **password**: password (min 6 characters)
    """
    return await user_service.create_user(user_create)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    """
    Login with email and password to get access token.
    
    - **username**: email address (OAuth2 uses 'username' field)
    - **password**: user password
    """
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = AuthService.create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return current_user

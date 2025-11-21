from .auth import router as auth_router
from .health import router as health_router
from .skills import router as skills_router
from .profile import router as profile_router
from .ai_routes import router as ai_router

__all__ = [
    "auth_router", 
    "health_router", 
    "skills_router", 
    "profile_router",
    "ai_router"
]

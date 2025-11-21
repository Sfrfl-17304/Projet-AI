from fastapi import APIRouter, Depends
from datetime import datetime
from config.settings import settings
from config.database import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check(db=Depends(get_db)):
    """
    Health check endpoint to verify API and database connectivity.
    
    Returns:
    - API status
    - Database connection status
    - Timestamp
    - Application version
    """
    # Check database connection
    try:
        await db.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "app_name": settings.app_name,
        "database": db_status
    }

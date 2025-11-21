from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
from routes.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/profile", tags=["User Profile"])


class InterestInput(BaseModel):
    """User interests and preferences."""
    interests: List[str]
    academic_background: str
    preferred_work_style: str
    strengths: List[str]


@router.get("/me")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile information.
    
    **Placeholder endpoint** - Will return full user profile with skills and progress.
    """
    return {
        "user": current_user,
        "profile": {
            "skills": ["Python", "FastAPI"],
            "completed_roadmap_items": 5,
            "current_learning_path": "Data Engineering",
            "progress_percentage": 25
        },
        "note": "Extended profile features to be implemented"
    }


@router.post("/interests")
async def submit_interests(
    interests: InterestInput,
    current_user: User = Depends(get_current_user)
):
    """
    Submit user interests for career recommendations (for beginners without CV).
    
    **Placeholder endpoint** - Will integrate with LLM for career matching.
    
    Returns recommended career paths based on interests.
    """
    return {
        "message": "Interest-based career recommendation endpoint - LLM integration pending",
        "user_id": current_user.id,
        "submitted_interests": interests.dict(),
        "recommended_careers": [
            {
                "role": "Data Engineer",
                "fit_score": 0.85,
                "reason": "Strong match with analytical interests and technical background"
            },
            {
                "role": "Backend Developer",
                "fit_score": 0.78,
                "reason": "Aligns with problem-solving strengths and technical skills"
            }
        ],
        "note": "This is placeholder data. Real recommendations will use LLM analysis."
    }


@router.get("/roadmap")
async def get_learning_roadmap(
    target_role: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized learning roadmap for a target role.
    
    **Placeholder endpoint** - Will generate time-aware roadmap based on skill gaps.
    
    - **target_role**: Target career role
    """
    return {
        "message": "Learning roadmap endpoint - Roadmap generation pending",
        "user_id": current_user.id,
        "target_role": target_role,
        "roadmap": {
            "phases": [
                {
                    "phase": "Foundation",
                    "duration": "2 months",
                    "skills": ["Python Basics", "SQL Fundamentals", "Git"]
                },
                {
                    "phase": "Intermediate",
                    "duration": "3 months",
                    "skills": ["Apache Spark", "Docker", "ETL Concepts"]
                },
                {
                    "phase": "Advanced",
                    "duration": "2 months",
                    "skills": ["Airflow", "Cloud Platforms", "Data Modeling"]
                }
            ],
            "total_duration": "7 months",
            "estimated_hours_per_week": 10
        },
        "note": "This is placeholder data. Real roadmap will be personalized and time-aware."
    }

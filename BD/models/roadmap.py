from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class RoadmapPhase(BaseModel):
    phase_number: int
    skills: List[str]
    duration_weeks: int
    resources: List[str] = Field(default_factory=list)

class Roadmap(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    target_role: str
    current_skills: List[str]
    timeline: str
    phases: List[RoadmapPhase]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }